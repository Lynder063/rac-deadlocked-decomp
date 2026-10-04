/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004978C0(s32);
u32 func_00498A98(s32, s32);
s32 func_00505B20();

u32 func_004C2EE0(s32 a0, s32 a1) {
    s32 temp_s1;

    temp_s1 = func_00505B20();
    return func_00498A98(temp_s1, func_004978C0(a0));
}
