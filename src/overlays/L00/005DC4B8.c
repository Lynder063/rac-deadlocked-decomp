/* cflags: -mno-split-addresses */
#include "common.h"

extern s32 D_00222410_[];
extern s32 D_00222420_[];
extern s32 D_00222430_[];
extern s32 D_00222440_[];
#define D_00222410 (D_00222410_[0])
#define D_00222420 (D_00222420_[0])
#define D_00222430 (D_00222430_[0])
#define D_00222440 (D_00222440_[0])

void func_L00_005DC4B8(void) {
    s32 *var_a0;
    s32 *var_a0_2;
    s32 *var_v1;
    s32 *var_v1_2;
    s32 var_v0;
    s32 var_v0_2;

    var_a0 = &D_00222420;
    var_v1 = &D_00222410;
    var_v0 = 3;
    do {
        *var_v1 = 0;
        var_v0 -= 1;
        *var_a0 = 0;
        var_v1 += 4;
        var_a0 += 4;
    } while (var_v0 >= 0);
    var_a0_2 = &D_00222440;
    var_v1_2 = &D_00222430;
    var_v0_2 = 3;
    do {
        *var_v1_2 = 0;
        var_v0_2 -= 1;
        *var_a0_2 = 0;
        var_v1_2 += 4;
        var_a0_2 += 4;
    } while (var_v0_2 >= 0);
}
