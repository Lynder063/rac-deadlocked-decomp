#include "common.h"

s32 func_004A3A28(s32);
s32 func_004A4D48();
s32 func_00501498(s32);
s32 func_00505AD8(s32);
s32 func_00505B20();
s32 func_00505C90(s32);
extern s32 D_307B30_[];
#define D_307B30 (D_307B30_[0])

void func_004A4DE8(s32 a0) {
    s32 temp_s0;

    if (D_307B30 == 0) {
        func_004A4D48();
    }
    D_307B30 |= 1 << a0;
    temp_s0 = func_00505B20();
    func_00505AD8(a0);
    func_00501498(func_004A3A28(a0));
    func_00505C90(func_004A3A28(a0));
    func_00505AD8(temp_s0);
}
