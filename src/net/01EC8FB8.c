#include "common.h"

s32 func_01EA06A8(s32);
extern s32 D_1B6A50_[];
#define D_1B6A50 (D_1B6A50_[0])

void func_01EC8FB8(s32 a0, s32 a1) {
    if (((u32) a1 < 0x100U) && (a0 != 0)) {
        func_01EA06A8(D_1B6A50 + (a1 * 4));
    }
}
