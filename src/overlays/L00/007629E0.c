/* cflags: -mno-split-addresses */
#include "common.h"

void func_L00_007629E0(s32 arg0, s32 *arg1) {
    s32 *var_a0;
    s32 *var_a1;
    s32 temp_v0;
    s32 var_v1;

    var_a1 = arg1;
    var_a0 = arg0 + 0x260;
    var_v1 = 3;
    do {
        temp_v0 = *var_a1;
        var_v1 -= 1;
        var_a1 += 4;
        *var_a0 = temp_v0;
        var_a0 += 4;
    } while (var_v1 >= 0);
}
