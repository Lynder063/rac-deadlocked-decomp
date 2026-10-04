/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004A2E48();
s32 func_005014B0(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();

void func_004A4DA0(void) {
    s32 temp_s0;

    temp_s0 = func_00505B20();
    func_00505AD8(4);
    func_005014B0(func_004A2E48());
    func_00505AD8(temp_s0);
}
