#include "common.h"

extern s32 D_00171BA8_[];

s32 func_004FC2C0(s32 a0) {
    s32 i;
    s32 n;

    n = 0;
    i = 0;
    do {
        n += (D_00171BA8_[(a0 - 1) % 20] >> i) & 1;
        i += 1;
    } while (i < 0xF);
    return n;
}
