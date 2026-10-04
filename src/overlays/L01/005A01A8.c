/* cflags: -mno-split-addresses */
#include "common.h"

f32 func_L00_005BCE18(f32);
f32 func_L00_005BCFE8(f32, f32);
s32 func_L00_005BD140(s32, s32, f32);

void func_L01_005A01A8(f32 *arg0, s32 arg1, s32 arg2, f32 fparg0) {
    f32 temp_f20;

    temp_f20 = (func_L00_005BCE18(*arg0) * 0.5f) + 0.5f;
    *arg0 = func_L00_005BCFE8(*arg0, fparg0);
    func_L00_005BD140(arg1, arg2, temp_f20);
}
