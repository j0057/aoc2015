#include <stdlib.h>

#include <openssl/md5.h>

#include "util.h"

int is_ok(char *hash, int difficulty) {
    int i = 0;
    while (difficulty > 0) {
        if ((hash[i] & (difficulty == 1 ? 0xf0 : 0xff)) > 0) {
            return 0;
        }
        difficulty -= 2;
        i++;
    }
    return 1;
}

int mine_coin(char *secret, int difficulty) {
    char buf[128] = {0};
    char md5[16] = {0};
    for (int i = 254575; i < 0xffffffff; i++) {
        int len = snprintf(buf, sizeof(buf), "%s%d", secret, i);
        MD5((unsigned char *)buf, len, (unsigned char *)md5);
        if (is_ok(md5, difficulty)) {
            return i;
        }
    }
    return 0;
}

int main(int argc, char *argv[]) {
    assert(mine_coin("abcdef",  5) == 609043);
    assert(mine_coin("pqrstuv", 5) == 1048970);

    char **day04 = NULL;
    int count;
    if (read_lines("../input/day04.txt", &day04, &count)) {
        return 1;
    }

    ANSWER(4, "a", mine_coin(day04[0], 5), 254575);
    ANSWER(4, "b", mine_coin(day04[0], 6), 1038736);

    for (int i = 0; i < count; i++) {
        free(day04[i]);
    }
    free(day04);
    return 0;
}
