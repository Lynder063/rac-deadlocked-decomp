#include "common.h"

extern s32 D_00354720_[];
#define D_00354720 (D_00354720_[0])

void *func_L01_00636D50(u32 arg0) {
    void *var_v1;

    var_v1 = NULL;
    if (arg0 < 0x40U) {
        var_v1 = (arg0 * 0x50) + &D_00354720;
    }
    return var_v1;
}
