#include "common.h"

s32 func_00453608(s32 *, s32, s32);
extern s32 D_31B6B0_[];
#define D_31B6B0 (D_31B6B0_[0])

void func_004D21F8(void) {
    s32 var_v0;

    func_00453608(&D_31B6B0, 0, 0x70);
    var_v0 = 3;
    do {
        var_v0 -= 1;
        D_31B6B0 = 2;
    } while (var_v0 >= 0);
}
