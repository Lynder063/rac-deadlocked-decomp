/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00453EB0(s16);
s32 func_004E1B18(s32);

void func_004E1AE8(s32 a0) {
    s32 temp_v0;

    temp_v0 = func_00453EB0((s16) a0);
    if (temp_v0 != 0) {
        func_004E1B18(temp_v0);
    }
}
