/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005CBF20(s32);

void func_L00_005CC540(void) {
    s32 var_s0;

    var_s0 = 0;
    do {
        func_L00_005CBF20(var_s0);
        var_s0 += 1;
    } while (var_s0 < 8);
}
