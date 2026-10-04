/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005BCFE8(f32, f32);
f32 func_L00_005BD030(f32, f32);

void func_L01_00594A10(f32 fparg0, f32 fparg1, f32 fparg2) {
    func_L00_005BCFE8(fparg0, func_L00_005BD030(fparg1, fparg0) * fparg2);
}
