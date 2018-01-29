
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <pcre.h>

#include "util.h"

typedef int (*is_nice_func_t)(char *s);

pcre *THREE_VOWELS = NULL;
pcre *ONE_DOUBLE = NULL;
pcre *NO_NAUGHTY = NULL;

pcre *TWO_PAIRS = NULL;
pcre *ONE_TRIPLET = NULL;

int compile_regexes() {
    return compile_regex(&THREE_VOWELS, "([aeiou])")
        || compile_regex(&ONE_DOUBLE, "(.)\\1")
        || compile_regex(&NO_NAUGHTY, "(ab|cd|pq|xy)")
        || compile_regex(&TWO_PAIRS, "(..).*\\1")
        || compile_regex(&ONE_TRIPLET, "(.).\\1");
}

void free_regexes() {
    FREE_REGEX(THREE_VOWELS);
    FREE_REGEX(ONE_DOUBLE);
    FREE_REGEX(NO_NAUGHTY);
    FREE_REGEX(TWO_PAIRS);
    FREE_REGEX(ONE_TRIPLET);
}

int count_matches(char *s, pcre *regex) {
    int r = 0;
    int ovector[12] = {0};
    while (1) {
        int rc = pcre_exec(regex, NULL, s, strlen(s), ovector[1], 0, ovector, 12);
        if (rc < 0)
            break;
        r += 1;
    }
    return r;
}

int is_nice(char *str) {
    return count_matches(str, THREE_VOWELS) >= 3
        && count_matches(str, ONE_DOUBLE) >= 1
        && count_matches(str, NO_NAUGHTY) == 0;
}

int is_new_nice(char *str) {
    return count_matches(str, TWO_PAIRS) >= 1
        && count_matches(str, ONE_TRIPLET) >= 1;
}

int count_nice_strings(char **strings, is_nice_func_t is_nice) {
    int r = 0;
    for (char **s = strings; *s != NULL; s++) {
        r += (*is_nice)(*s);
    }
    return r;
}

int main(int argc, char *argv[]) {
    if (compile_regexes()) {
        free_regexes();
        return 1;
    }

    assert(!is_nice("xxx"));
    assert(is_nice("ugknbfddgicrmopn"));
    assert(is_nice("aaa"));
    assert(!is_nice("jchzalrnumimnmhp"));
    assert(!is_nice("haegwjzuvuyypxyu"));
    assert(!is_nice("dvszwmarrgswjxmb"));

    assert(is_new_nice("qjhvhtzxzqqjkmpb"));
    assert(is_new_nice("xxyxx"));
    assert(!is_new_nice("uurcxstgmygtbstg"));
    assert(!is_new_nice("ieodomkazucvgmuy"));

    char **day05 = NULL;
    if (read_lines("../input/day05.txt", &day05)) {
        return 1;
    }

    ANSWER(5, "a", count_nice_strings(day05, &is_nice),     238);
    ANSWER(5, "b", count_nice_strings(day05, &is_new_nice),  69);

    free(day05);
    free_regexes();
    return 0;
}
