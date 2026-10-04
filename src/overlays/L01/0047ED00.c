#include "common.h"

s32 func_L01_0047ECC8(s32, s32);
extern s32 D_0039D300_[];
#define D_0039D300 (D_0039D300_[0])

s32 func_L01_0047ED00(s32 arg0) {
    s32 *var_v1;
    s32 var_a0;

    var_v1 = &D_0039D300;
    var_a0 = 0;
loop_1:
    if (*var_v1 != arg0) {
        var_a0 += 1;
        var_v1 += 4;
        if (var_a0 >= 0x19) {
            return 0;
        }
        goto loop_1;
    }
    func_L01_0047ECC8(var_a0, arg0);
    return 1;
}
