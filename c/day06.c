#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "util.h"

typedef void (*op_func_t)(int *grid, int x, int y);

int run_grid(char **script, op_func_t op_on, op_func_t op_toggle, op_func_t op_off) {
    int *grid = calloc(1000 * 1000, sizeof(int));
    int x1, y1, x2, y2;
    op_func_t op_func;

    for (char **op = script; *op != NULL; op++) {
        if (sscanf(*op, "turn on %d,%d through %d,%d", &x1, &y1, &x2, &y2)) {
            op_func = op_on;
        }
        else if (sscanf(*op, "toggle %d,%d through %d,%d", &x1, &y1, &x2, &y2)) {
            op_func = op_toggle;
        }
        else if (sscanf(*op, "turn off %d,%d through %d,%d", &x1, &y1, &x2, &y2)) {
            op_func = op_off;
        }
        else {
            fprintf(stderr, "error: could not parse '%s'!\n", *op);
            free(grid);
            return -1;
        }

        for (int y = y1; y <= y2; y++) {
            for (int x = x1; x <= x2; x++) {
                (*op_func)(grid, x, y);
            }
        }
    }

    int r = 0;
    for (int y = 0; y < 1000; y++) {
        for (int x = 0; x < 1000; x++) {
            r += *(grid + y * 1000 + x);
        }
    }

    free(grid);
    return r;
}

void op_on_1(int *grid, int x, int y) {
    *(grid + y * 1000 + x) = 1;
}

void op_toggle_1(int *grid, int x, int y) {
    *(grid + y * 1000 + x) = 1 - *(grid + y * 1000 + x);
}

void op_off_1(int *grid, int x, int y) {
    *(grid + y * 1000 + x) = 0;
}

void op_on_2(int *grid, int x, int y) {
    *(grid + y * 1000 + x) += 1;
}

void op_toggle_2(int *grid, int x, int y) {
    *(grid + y * 1000 + x) += 2;
}

void op_off_2(int *grid, int x, int y) {
    *(grid + y * 1000 + x) = *(grid + y * 1000 + x)
        ? *(grid + y * 1000 + x) - 1
        : 0;
}

int run_grid_1(char **script) {
    return run_grid(script, &op_on_1, &op_toggle_1, &op_off_1);
}

int run_grid_2(char **script) {
    return run_grid(script, &op_on_2, &op_toggle_2, &op_off_2);
}

int main(int argc, char *argv[]) {
    char *ex_1a[] = { "turn on 0,0 through 999,999", NULL };
    char *ex_1b[] = { "toggle 0,0 through 999,0", NULL };
    char *ex_1c[] = { "turn on 0,0 through 999,999", "turn off 499,499 through 500,500", NULL };

    assert(run_grid_1(ex_1a) == 1000000);
    assert(run_grid_1(ex_1b) ==    1000);
    assert(run_grid_1(ex_1c) ==  999996);

    char **day06 = NULL;
    if (read_lines("../input/day06.txt", &day06)) {
        return 1;
    }

    ANSWER(6, "a", run_grid_1(day06),   569999);
    ANSWER(6, "b", run_grid_2(day06), 17836115);

    free(day06);
    return 0;
}
