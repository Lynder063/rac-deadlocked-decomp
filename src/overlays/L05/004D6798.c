/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005BD140(s32, s32, f32);

void func_L05_004D6798(s32 arg0, s32 arg1, s32 arg2, f32 fparg0) {
    s32 *var_s0;
    s32 var_s1;

    var_s0 = arg0 + 0x40;
    var_s1 = 3;
    do {
        var_s1 -= 1;
        *var_s0 = func_L00_005BD140(arg1, arg2, fparg0);
        var_s0 += 4;
    } while (var_s1 >= 0);
}
