/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004B54D8();
s32 func_00505AD8(s32);
s32 func_00505B20();

void func_0049A8D8(void) {
    s32 temp_s0;

    temp_s0 = func_00505B20();
    func_00505AD8(0);
    func_00505AD8(temp_s0);
    func_004B54D8();
}
