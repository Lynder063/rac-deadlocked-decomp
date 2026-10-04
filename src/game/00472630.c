/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00163408();

f32 func_00472630(f32 a0, f32 a1) {
    f32 var_f0;
    s32 temp_v0;

    temp_v0 = func_00163408();
    var_f0 = a0 + ((f32) temp_v0 * (a1 - a0) * 0.000030517578f);
    if (temp_v0 & 1) {
        var_f0 = -var_f0;
    }
    return var_f0;
}
