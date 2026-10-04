#include "common.h"

s32 func_L01_004EBD40(s32 unused, char *p) {
    s32 *q;
    s32 n;
    s32 i;

    q = (s32 *)(p + 0x378);
    n = 0;
    i = 5;
    do {
        s32 v = *q;
        q += 1;
        i -= 1;
        if (v != 0) {
            n += 1;
        }
    } while (i >= 0);
    return n;
}
