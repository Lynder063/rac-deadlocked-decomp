/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00496D20(s32, s32, s32);
s32 func_00547AC8(s32);

void func_00547A40(s32 a0, s32 a1, s32 a2) {
    if (func_00547AC8(a1) != 0) {
        func_00496D20(a0, a1, a2);
    }
}
