
#include <assert.h>
#include <stdio.h>

/*
 * assertion helpers
 */

#define _ANSWER(day, part, expression, expected, fmt) { \
    int answer = expression; \
    printf(fmt, day, part, answer); \
    assert(answer == expected); \
}

#define ANSWER(day, part, expression, expected) _ANSWER(day, part, expression, expected, "%d%s = %d\n")

/*
 * file input helpers
 */

int read_file(char *path, char **buf);

int read_lines(char *path, char ***lines);

/*
 * helpers for pcre, if using them
 */

#ifdef _PCRE_H

int compile_regex(pcre **regex, char *pattern) {
    const char *error = NULL;
    int error_pos = 0;

    *regex = pcre_compile(pattern, 0, &error, &error_pos, NULL);
    if (*regex == NULL) {
        fprintf(stderr, "regex error at pos %d: %s\n", error_pos, error);
        return 1;
    }

    return 0;
}

#define FREE_REGEX(r) { if (r) { pcre_free(r); r = NULL; } }

#endif
