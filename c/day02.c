
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#include "util.h"

int min(int a, int b) { return a<b ? a : b; }

typedef int (*calc_func_t)(int l, int w, int h);

int parse_line(char *line, int *l, int *w, int *h) {
    if (sscanf(line, "%dx%dx%d", l, w, h) != 3) {
        fprintf(stderr, "error: unable to parse line '%s'", line);
        return 1;
    }
    return 0;
}

int calc_paper(int l, int w, int h) {
    int s1 = l * w;
    int s2 = w * h;
    int s3 = h * l;

    return 2 * s1 + 2 * s2 + 2 * s3 + min(s1, min(s2, s3));
}

int calc_ribbon(int l, int w, int h) {
    return min(2 * l + 2 * w, min(2 * w + 2 * h, 2 * h + 2 * l))  +  w * h * l;
}

int sum_by(char **lines, calc_func_t calc){
    int sum = 0;
    for (char **line = lines; *line != NULL; line++) {
        int l, w, h;
        if (parse_line(*line, &l, &w, &h)) {
            return 1;
        }
        sum += (*calc)(l, w, h);
    }
    return sum;
}


int main(int argc, char *argv[]) {
    assert(calc_paper(2, 3, 4)  == 58);
    assert(calc_paper(1, 1, 10) == 43);

    assert(calc_ribbon(2, 3, 4)  == 34);
    assert(calc_ribbon(1, 1, 10) == 14);

    char **day03 = NULL;
    if (read_lines("../input/day02.txt", &day03)) {
        return 1;
    }

    ANSWER(2, "a", sum_by(day03, &calc_paper),  1598415);
    ANSWER(2, "b", sum_by(day03, &calc_ribbon), 3812909);

    free(day03);
}
