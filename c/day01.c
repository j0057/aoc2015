#include <stdio.h>
#include <stdlib.h>

#include <assert.h>

#include "util.h"

int count_floors(char *dir) {
    int floor = 0;
    for (char *ch = dir; *ch; ch++) {
        floor += *ch == '(' ? +1
               : *ch == ')' ? -1 : 0;
    }
    return floor;
}

int find_basement(char *dir) {
    int floor = 0;
    for (char *ch = dir; *ch; ch++) {
        floor += *ch == '(' ? +1
               : *ch == ')' ? -1 : 0;
        if (floor < 0) {
            return ch - dir + 1;
        }
    }
    return -1;
}

int main(int argc, char *argv[]) {
    assert(count_floors("(())")    ==  0);
    assert(count_floors("()()")    ==  0);
    assert(count_floors("(((")     ==  3);
    assert(count_floors("(()(()(") ==  3);
    assert(count_floors("))(((((") ==  3);
    assert(count_floors("())")     == -1);
    assert(count_floors("))(")     == -1);
    assert(count_floors(")))")     == -3);
    assert(count_floors(")())())") == -3);

    assert(find_basement(")")     == 1);
    assert(find_basement("()())") == 5);

    char *day01 = NULL;
    if (read_file("../input/day01.txt", &day01)) {
        return 1;
    }

    ANSWER(1, "a", count_floors(day01), 232);
    ANSWER(1, "b", find_basement(day01), 1783);

    free(day01);
    return 0;
}
