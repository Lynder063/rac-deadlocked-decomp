#include "common.h"

s32 func_004AFE50();
s32 func_00501498(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();
s32 func_00505C90(s32);
extern s32 D_3095B0_[];
#define D_3095B0 (D_3095B0_[0])

void func_004AFF38(s32 a0) {
    s32 temp_s0;

    if (D_3095B0 == 0) {
        temp_s0 = func_00505B20();
        func_00505AD8(4);
        func_00501498(func_004AFE50());
        func_00505C90(func_004AFE50());
        func_00505AD8(temp_s0);
    }
    D_3095B0 |= 1 << a0;
}
