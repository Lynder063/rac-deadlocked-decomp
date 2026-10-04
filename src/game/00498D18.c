#include "common.h"

s32 func_00453608(void *, s32, s32);
extern s32 D_2F3408_[];
#define D_2F3408 (D_2F3408_[0])

void func_00498D18(void) {
    s32 *var_s0;
    s32 var_v0;

    func_00453608(&D_2F3408, 0, 0xC4);
    var_s0 = &D_2F3408 + 0x78;
    var_v0 = 9;
    do {
        *var_s0 = -1;
        var_v0 -= 1;
        var_s0 -= 0xC;
    } while (var_v0 >= 0);
}
