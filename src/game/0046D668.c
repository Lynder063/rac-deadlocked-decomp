#include "common.h"

s32 func_0046D7D8(s32);
extern s32 D_266AA8_[];
#define D_266AA8 (D_266AA8_[0])

void func_0046D668(void) {
    s32 var_s0;

    var_s0 = 0;
    D_266AA8 = 0;
    do {
        func_0046D7D8(var_s0);
        var_s0 += 1;
    } while (var_s0 < 8);
}
