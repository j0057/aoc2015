#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <complex.h>

#include "util.h"

typedef double _Complex coord_t;

int count_houses(int size, char *route, int actors) {
    uint64_t *houses = calloc(size * size, sizeof(uint64_t *));

    size_t route_len = strlen(route);

    for (int i = 0; i < actors; i++) {
        coord_t pos = size/2 + size/2 * I;

        *(houses + (int)(creal(pos)) * size + ((int)cimag(pos))) += 1;
        for (char *ch = route + i; (ch - route) <= route_len; ch += actors) {
            switch (*ch) {
                case '^': pos +=  0-1*I; break;
                case 'v': pos +=  0+1*I; break;
                case '<': pos += -1+0*I; break;
                case '>': pos += +1+0*I; break;
            }
            *(houses + (int)(creal(pos)) * size + ((int)cimag(pos))) += 1;
        }
    }

    int r = 0;
    for (int i = 0; i < size * size; i++) {
        r += houses[i] > 0;
    }

    free(houses);
    return r;
}

int main(int argc, char *argv[]) {
    assert(count_houses(128, ">",        1) == 2);
    assert(count_houses(128, "^>v<",     1) == 4);
    assert(count_houses(128, "^v^v^v^v", 1) == 2);

    assert(count_houses(128, "^v",         2) == 3);
    assert(count_houses(128, "^>v<",       2) == 3);
    assert(count_houses(128, "^v^v^v^v^v", 2) == 11);

    char *day03 = NULL;
    if (read_file("../input/day03.txt", &day03)) {
        return 1;
    }

    ANSWER(3, "a", count_houses(256, day03, 1), 2565);
    ANSWER(3, "b", count_houses(256, day03, 2), 2639);

    free(day03);
    return 0;
}
