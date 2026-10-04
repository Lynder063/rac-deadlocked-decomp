/* cflags: -mno-split-addresses */
#include "common.h"

void func_00524BF0(s32 a0, s32 a1, s32 a2, f32 a3);
void func_00524CA0(s32 a0, s32 a1, s32 a2, f32 a3);
void func_00524E70(s32 a0, s32 a1, s32 a2, f32 a3);

s32 func_00524DC0(s32, s32, s32, f32);

void func_00517B28(s32 a0, s32 a1, f32 a2, f32 a3, s32 a4) {
    if (a4 != 0) {
        func_00524E70(a0, a1, a1, a2);
        func_00524DC0(a0, a1, a1, a3);
        return;
    }
    func_00524CA0(a0, a1, a1, a2);
    func_00524BF0(a0, a1, a1, a3);
}
