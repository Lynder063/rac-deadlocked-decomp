#include "common.h"

s32 func_0011A370(void *, s32, s32);
extern s32 D_1AFD28_[];
#define D_1AFD28 (D_1AFD28_[0])

s32 func_01EA3778(s32 a0) {
    s32 var_v0;

    var_v0 = 0x17;
    if (a0 != 0) {
        func_0011A370(&D_1AFD28, a0, 0x18);
        var_v0 = 0;
    }
    return var_v0;
}
