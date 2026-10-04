/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L01_004537F8(s32 arg0) {
    s32 temp_v1;
    s32 var_a0;
    s32 var_a1;

    var_a0 = arg0;
    var_a1 = 0;
    if (var_a0 > 0) {
        do {
            temp_v1 = var_a0 & 1;
            var_a0 = (s32) (var_a0 + ((u32) var_a0 >> 0x1F)) >> 1;
            var_a1 += temp_v1;
        } while (var_a0 > 0);
    }
    return var_a1;
}
