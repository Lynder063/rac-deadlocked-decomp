/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497980(s32);
s32 func_004CB620(s32);
s32 func_004CD048();
s32 func_00501498(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();
s32 func_00505C90(s32);

void func_004CB798(s32 a0) {
    s32 temp_s1;

    temp_s1 = func_00505B20();
    func_00505AD8(a0);
    func_00501498(func_004CB620(a0));
    func_00505C90(func_004CB620(a0));
    func_00505AD8(temp_s1);
    func_00497980(5);
    func_004CD048();
}
