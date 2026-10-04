/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497908(s32, s32);
s32 func_0049A6B0(s32, s32);
s32 func_004AD1B8();
s32 func_00505B20();

void func_004AA068(s32 a0) {
    s32 temp_s0;

    temp_s0 = func_00505B20();
    func_004AD1B8();
    func_00497908(temp_s0, 0x18);
    func_0049A6B0(temp_s0, 0x10);
}
