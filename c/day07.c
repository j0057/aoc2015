#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#include <assert.h>

#include <gmodule.h>

#include "util.h"

#define OP_SET 1    // source is reg or imm
#define OP_AND 2    // source1 is reg or imm; source2 always reg
#define OP_OR  3    // source1-2 are always imm
#define OP_NOT 4    // source is reg
#define OP_SHL 5    // source1 is reg, source2 is imm
#define OP_SHR 6    // source1 is reg, source2 is imm

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

        if (sscanf(*s, "%s AND %s -> %s", wire->binary.source1, wire->binary.source2, wire->target)) {
            wire->type = OP_AND;
        }
        else if (sscanf(*s, "%s OR %s -> %s", wire->binary.source1, wire->binary.source2, wire->target)) {
            wire->type = OP_OR;
        }
        else if (sscanf(*s, "NOT %s -> %s", wire->unary.source, wire->target)) {
            wire->type = OP_NOT;
        }
        else if (sscanf(*s, "%s LSHIFT %s -> %s", wire->binary.source1, wire->binary.source2, wire->target)) {
            wire->type = OP_SHL;
        }
        else if (sscanf(*s, "%s RSHIFT %s -> %s", wire->binary.source1, wire->binary.source2, wire->target)) {
            wire->type = OP_SHR;
        }
        else if (sscanf(*s, "%s -> %s", wire->unary.source, wire->target)) {
            wire->type = OP_SET;
        }
        else {
            fprintf(stderr, "could not parse wire '%s'\n", *s);
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

uint64_t evaluate(GHashTable *wires, GHashTable *value, char *wire_name) {
    if (g_hash_table_contains(value, wire_name)) {
        return (uint64_t)g_hash_table_lookup(value, wire_name);
    }

    wire_t *wire = g_hash_table_lookup(wires, wire_name);

    switch (wire->type) {
        case OP_SET:
            g_hash_table_insert(value, wire->target, str_is_number(wire->unary.source)
                ? (gpointer)strtol(wire->unary.source, NULL, 10)
                : (gpointer)evaluate(wires, value, wire->unary.source));
            break;

        case OP_AND: {
            uint64_t value1 = str_is_number(wire->binary.source1)
                ? strtol(wire->binary.source1, NULL, 10)
                : evaluate(wires, value, wire->binary.source1);
            uint64_t value2 = str_is_number(wire->binary.source1)
                ? strtol(wire->binary.source2, NULL, 10)
                : evaluate(wires, value, wire->binary.source2);
            g_hash_table_insert(value, wire->target, (gpointer)(value1 & value2));
            break;
        }

        default:
            fprintf(stderr, "unknown wire type %d\n", wire->type);
            return 0xffffffff;
    }

    return (uint64_t)g_hash_table_lookup(value, wire_name);
}

uint64_t run_circuit(char **spec, char *wire) {
    GHashTable *wires = g_hash_table_new_full(&g_str_hash, &g_str_equal, NULL, free);
    GHashTable *value = g_hash_table_new_full(&g_str_hash, &g_str_equal, NULL, NULL);

    if (parse_circuit(wires, spec)) {
        g_hash_table_destroy(wires);
        g_hash_table_destroy(value);
        return 0xffffffff;
    }

    uint64_t result = evaluate(wires, value, wire);

    g_hash_table_destroy(wires);
    g_hash_table_destroy(value);

    return result;
}

int main(int argc, char *argv[]) {
    //char *ex0[] = { "123 -> x", NULL };
    char *ex1[] = {
        "123 -> x",
        "456 -> y",
        "x AND y -> d",
        "x OR y -> e",
        "x LSHIFT 2 -> f",
        "y LSHIFT 2 -> g",
        "NOT x -> h",
        "NOT y -> i",
        NULL
    };

    //assert(run_circuit(ex0, "x") ==   123);
    assert(run_circuit(ex1, "d") ==    72);
    //assert(run_circuit(ex1, "e") ==   507);
    //assert(run_circuit(ex1, "f") ==   492);
    //assert(run_circuit(ex1, "g") ==   114);
    //assert(run_circuit(ex1, "h") == 65412);
    //assert(run_circuit(ex1, "i") == 65079);
    assert(run_circuit(ex1, "x") ==   123);
    assert(run_circuit(ex1, "y") ==   456);

    //char **day07 = NULL;
    //if (read_lines("../input/day07.txt", &day07)) {
    //    return 1;
    //}

    //free(day07);
    return 0;
}
