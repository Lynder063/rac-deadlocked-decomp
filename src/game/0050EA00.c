/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_005015B0();
extern s32 D_00220B50_[];
#define D_00220B50 (D_00220B50_[0])

s32 func_0050EA00(s32 a0, u32 a1) {
    s32 var_v0;

    if (a1 != 2) {
        if (D_00220B50 == a1) {
            var_v0 = 1;
        } else {
            var_v0 = func_005015B0();
        }
        return var_v0 & 0xFF;
    }
    return 1;
}
