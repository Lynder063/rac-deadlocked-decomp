/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00453608(void *, s32, s32);
extern s32 D_2217B8_[];
extern s32 D_2217BC_[];
extern s32 D_2217C0_[];
#define D_2217B8 (D_2217B8_[0])
#define D_2217BC (D_2217BC_[0])
#define D_2217C0 (D_2217C0_[0])

void func_004B9140(void) {
    s32 *var_a0;
    s32 *var_v1;
    s32 var_v0;

    func_00453608(&D_2217B8, 0, 0x10);
    var_a0 = &D_2217C0;
    var_v1 = &D_2217BC;
    var_v0 = 0;
    do {
        *var_v1 = 1;
        var_v0 -= 1;
        *var_a0 = 0;
        var_v1 += 0x10;
        var_a0 += 0x10;
    } while (var_v0 >= 0);
}
