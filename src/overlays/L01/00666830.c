#include "common.h"

s32 func_L01_00666888(s32);
extern s32 D_003660F8_[];
#define D_003660F8 (D_003660F8_[0])

void func_L01_00666830(void) {
    s32 *var_s0;
    s32 var_s1;
    s32 var_v1;

    var_s0 = &D_003660F8;
    var_s1 = 9;
    var_v1 = D_003660F8;
    do {
        var_s0 += 4;
        var_s1 -= 1;
        if (var_v1 != 0) {
            func_L01_00666888(var_v1);
        }
        var_v1 = *var_s0;
    } while (var_s1 >= 0);
}
