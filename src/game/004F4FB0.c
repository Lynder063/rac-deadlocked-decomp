#include "common.h"

s32 func_00464038(s32);
s32 func_004F3468();
s32 func_004F4B88();
extern s32 D_1DFC54_[];
#define D_1DFC54 (D_1DFC54_[0])

void func_004F4FB0(s32 a0) {
    func_004F3468();
    D_1DFC54 = a0;
    func_00464038(0);
    func_004F4B88();
}
