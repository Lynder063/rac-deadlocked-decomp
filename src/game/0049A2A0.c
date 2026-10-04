/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00499DF8(s32);
s32 func_00501498(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();
s32 func_00505C90(s32);

void func_0049A2A0(s32 a0) {
    s32 temp_s1;

    temp_s1 = func_00505B20();
    func_00505AD8(a0);
    func_00501498(func_00499DF8(a0));
    func_00505C90(func_00499DF8(a0));
    func_00505AD8(temp_s1);
}
