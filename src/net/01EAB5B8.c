#include "common.h"

s32 func_01EAB3C0(void);
s32 func_01EAB610(s32 a0, void * a1);

extern u8 D_00168BA0_[];
extern s32 D_1B23E0_[];
#define D_00168BA0 (D_00168BA0_[0])
#define D_1B23E0 (D_1B23E0_[0])

s32 func_01EAB5B8(void *a0) {
    s32 var_v0;

    var_v0 = 2;
    if (a0 != NULL) {
        if (D_00168BA0 == 0) {
            var_v0 = func_01EAB3C0();
            if (var_v0 == 0) {
                goto block_4;
            }
        } else {
block_4:
            var_v0 = func_01EAB610((s32) &D_1B23E0, a0);
        }
    }
    return var_v0;
}
