#include "common.h"

void func_004A4DA0(void);
s32 func_00505AD8(s32 a0);
s32 func_00505B20(void);

s32 func_004A3A28(s32);
s32 func_005014B0(s32);
extern s32 D_307B30_[];
#define D_307B30 (D_307B30_[0])

void func_004A4E70(s32 a0) {
    s32 temp_a0;
    s32 temp_s0;

    temp_a0 = D_307B30 & ~(1 << a0);
    D_307B30 = temp_a0;
    if (temp_a0 == 0) {
        func_004A4DA0();
    }
    temp_s0 = func_00505B20();
    func_00505AD8(a0);
    func_005014B0(func_004A3A28(a0));
    func_00505AD8(temp_s0);
}
