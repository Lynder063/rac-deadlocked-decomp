/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0049A938(s32);
s32 func_00501498(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();
s32 func_00505C90(s32);
extern s32 D_0021EDD4_[];
#define D_0021EDD4 (D_0021EDD4_[0])

void func_0049AB48(s32 a0) {
    s32 temp_s0;
    s32 temp_s1;

    temp_s0 = ((D_0021EDD4 ^ 1) == 0) ? a0 : 0;
    temp_s1 = func_00505B20();
    func_00505AD8(temp_s0);
    func_00501498(func_0049A938(temp_s0));
    func_00505C90(func_0049A938(temp_s0));
    func_00505AD8(temp_s1);
}
