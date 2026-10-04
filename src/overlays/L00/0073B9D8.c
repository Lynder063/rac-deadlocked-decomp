/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_0073B9D8(s32 *arg0) {
    s32 *var_a0;
    s32 temp_v0;
    s32 var_a1;
    s32 var_v1;

    var_v1 = *arg0;
    var_a1 = 2;
    var_a0 = arg0 + 4;
    do {
        temp_v0 = *var_a0;
        var_a1 -= 1;
        var_a0 += 4;
        var_v1 += temp_v0;
    } while (var_a1 >= 0);
    return var_v1;
}
