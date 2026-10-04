#include "common.h"

void func_004764B8(s32 *a, s32 *b, s32 *c, s32 mask) {
    s32 t;

    if (mask & 1) {
        t = *a;
        *a = *b;
        *b = t;
    }
    if (mask & 2) {
        t = *b;
        *b = *c;
        *c = t;
    }
    if (mask & 4) {
        t = *c;
        *c = *a;
        *a = t;
    }
}
