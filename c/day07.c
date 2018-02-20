#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include <assert.h>
#include <setjmp.h>

#include <gmodule.h>

#include "util.h"

#define OP_SET 1    // source is reg or imm
#define OP_AND 2    // source1 is reg or imm; source2 always reg
#define OP_OR  3    // source1-2 are always imm
#define OP_NOT 4    // source is reg
#define OP_SHL 5    // source1 is reg, source2 is imm
#define OP_SHR 6    // source1 is reg, source2 is imm

jmp_buf EVALUATE_ERROR = {0};
jmp_buf RUN_CIRCUIT_ERROR = {0};

typedef struct op_unary_struct_t {
    char source[8];
} op_unary_t;

typedef struct op_binary_struct_t {
    char source1[8];
    char source2[8];
} op_binary_t;

typedef struct wire_struct_t {
    int type;
    char target[8];
    union {
        op_unary_t unary;
        op_binary_t binary;
    };
} wire_t;

int parse_circuit(GHashTable *circuit, char **spec) {
    for (char **s = spec; *s != NULL; s++) {

        wire_t *wire = calloc(1, sizeof(wire_t));

        if (sscanf(*s, "%s -> %s", wire->unary.source, wire->target) == 2) {
            wire->type = OP_SET;
        }
        else if (sscanf(*s, "%s AND %s -> %s", wire->binary.source1, wire->binary.source2, wire->target) == 3) {
            wire->type = OP_AND;
        }
        else if (sscanf(*s, "%s OR %s -> %s", wire->binary.source1, wire->binary.source2, wire->target) == 3) {
            wire->type = OP_OR;
        }
        else if (sscanf(*s, "NOT %s -> %s", wire->unary.source, wire->target) == 2) {
            wire->type = OP_NOT;
        }
        else if (sscanf(*s, "%s LSHIFT %s -> %s", wire->binary.source1, wire->binary.source2, wire->target) == 3) {
            wire->type = OP_SHL;
        }
        else if (sscanf(*s, "%s RSHIFT %s -> %s", wire->binary.source1, wire->binary.source2, wire->target) == 3) {
            wire->type = OP_SHR;
        }
        else {
            fprintf(stderr, "error: could not parse wire '%s'\n", *s);
            return 1;
        }

        g_hash_table_insert(circuit, wire->target, wire);
    }
    return 0;
}

static inline int str_is_number(char *str) {
    char *end = NULL;
    strtol(str, &end, 10);
    return *end == '\0';
}

#define eval(s) (str_is_number(s) ? strtol(s, NULL, 10) : evaluate(wires, value, s))

uint16_t evaluate(GHashTable *wires, GHashTable *value, char *wire_name) {
    if (g_hash_table_contains(value, wire_name)) {
        return (uint16_t)(uint64_t)g_hash_table_lookup(value, wire_name);
    }

    wire_t *wire = g_hash_table_lookup(wires, wire_name);
    if (wire == NULL) {
        fprintf(stderr, "error: could not find wire %s!\n", wire_name);
        longjmp(EVALUATE_ERROR, 0);
    }

    uint16_t result;
    switch (wire->type) {
        case OP_SET:
            result = eval(wire->unary.source);
            break;

        case OP_AND:
            result = eval(wire->binary.source1) & eval(wire->binary.source2);
            break;

        case OP_OR:
            result = eval(wire->binary.source1) | eval(wire->binary.source2);
            break;

        case OP_NOT:
            result = eval(wire->unary.source) ^ 0xffff;
            break;

        case OP_SHL:
            result = eval(wire->binary.source1) << eval(wire->binary.source2);
            break;

        case OP_SHR:
            result = eval(wire->binary.source1) >> eval(wire->binary.source2);
            break;

        default:
            fprintf(stderr, "error: unknown wire type %d\n", wire->type);
            longjmp(EVALUATE_ERROR, 0);
    }

    g_hash_table_insert(value, wire->target, (gpointer)(uint64_t)result);

    return result;
}

#undef eval

void init_hashes(GHashTable **wires, GHashTable **value) {
    *wires = g_hash_table_new_full(&g_str_hash, &g_str_equal, NULL, free);
    *value = g_hash_table_new_full(&g_str_hash, &g_str_equal, NULL, NULL);
}

void free_hashes(GHashTable **wires, GHashTable **cache) {
    g_hash_table_destroy(*wires); *wires = NULL;
    g_hash_table_destroy(*cache); *cache = NULL;
}

int64_t run_circuit_2(char **spec, char *wire, char *hack_target, uint16_t hack_value) {
    GHashTable *wires = NULL, *cache = NULL;

    init_hashes(&wires, &cache);

    if (parse_circuit(wires, spec)) {
        free_hashes(&wires, &cache);
        return 0xffffffffffffffff;
    }

    if (hack_target != NULL) {
        wire_t *hack_wire = calloc(1, sizeof(wire_t));
        hack_wire->type = OP_SET;
        strcpy(hack_wire->target, hack_target);
        sprintf(hack_wire->unary.source, "%d", hack_value);
        g_hash_table_replace(wires, hack_target, hack_wire);
    }

    if (setjmp(EVALUATE_ERROR)) {
        free_hashes(&wires, &cache);
        return 0xffffffffffffffff;
    }

    uint16_t result = evaluate(wires, cache, wire);
    free_hashes(&wires, &cache);
    return result;
}

uint64_t run_circuit_1(char **spec, char *wire) {
    return run_circuit_2(spec, wire, NULL, 0);
}

#define test_wire_hash(w, t) { \
    wire_t *wire = g_hash_table_lookup(wires, w); \
    assert(wire != NULL); \
    assert(strcmp(wire->target, w) == 0); \
    assert(wire->type == t); \
}

void test_parser_ex1(char **ex1) {
    GHashTable *wires = g_hash_table_new_full(&g_str_hash, &g_str_equal, NULL, free);

    assert(parse_circuit(wires, ex1) == 0);

    test_wire_hash("x", OP_SET);
    test_wire_hash("y", OP_SET);
    test_wire_hash("d", OP_AND);
    test_wire_hash("e", OP_OR);
    test_wire_hash("f", OP_SHL);
    test_wire_hash("g", OP_SHR);
    test_wire_hash("h", OP_NOT);
    test_wire_hash("i", OP_NOT);

    g_hash_table_destroy(wires);
}

#undef test_wire_hash

int main(int argc, char *argv[]) {
    char *ex0[] = {
        "123 -> x",
        "65412 -> y",
        "x OR y -> z",
        NULL
    };

    char *exE[] = {
        "blueagrh",
        NULL
    };

    char *ex1[] = {
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y RSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i",
        NULL
    };

    test_parser_ex1(ex1);

    assert(run_circuit_1(ex0, "x") ==   123);
    assert(run_circuit_1(ex0, "y") == 65412);
    assert(run_circuit_1(ex0, "z") == 65535);

    assert(run_circuit_1(exE, "_") != 65535);

    assert(run_circuit_1(ex1, "x") ==   123);
    assert(run_circuit_1(ex1, "y") ==   456);
    assert(run_circuit_1(ex1, "d") ==    72);
    assert(run_circuit_1(ex1, "e") ==   507);
    assert(run_circuit_1(ex1, "f") ==   492);
    assert(run_circuit_1(ex1, "g") ==   114);
    assert(run_circuit_1(ex1, "h") == 65412);
    assert(run_circuit_1(ex1, "i") == 65079);

    char **day07 = NULL;
    if (read_lines("../input/day07.txt", &day07)) {
        return 1;
    }

    ANSWER(7, "a", run_circuit_1(day07, "a"),             46065);
    ANSWER(7, "b", run_circuit_2(day07, "a", "b", 46065), 14134);

    free(day07);
    return 0;
}
