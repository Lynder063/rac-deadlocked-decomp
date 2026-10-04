/* cflags: -mno-split-addresses */
#include "common.h"

u32 func_L00_0077CFE0(u32 arg0, u32 arg1) {
    u32 temp_hi;
    u32 var_a0;

    var_a0 = arg0;
    temp_hi = var_a0 % arg1;
    if (temp_hi != 0) {
        var_a0 += arg1 - temp_hi;
    }
    return var_a0;
}
