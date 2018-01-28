
#include <assert.h>
#include <stdio.h>

#define _ANSWER(day, part, expression, expected, fmt) { \
    int answer = expression; \
    printf(fmt, day, part, answer); \
    assert(answer == expected); \
}

#define ANSWER(day, part, expression, expected) _ANSWER(day, part, expression, expected, "%d%s = %d\n")

int read_file(char *path, char **buf);

int read_lines(char *path, char ***lines, int *count);
int read_lines_2(char *path, char ***lines, int *count);
