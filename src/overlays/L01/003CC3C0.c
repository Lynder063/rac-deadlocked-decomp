/* cflags: -mno-split-addresses */
#include "common.h"

s32 *func_L01_00584068(s32);

s32 func_L01_003CC3C0(s32 arg0) {
    s32 var_s0;

    var_s0 = 0;
loop_1:
    if (*func_L01_00584068(var_s0) != arg0) {
        var_s0 += 1;
        if (var_s0 >= 0x40) {
            return -1;
        }
        goto loop_1;
    }
    return var_s0;
}
