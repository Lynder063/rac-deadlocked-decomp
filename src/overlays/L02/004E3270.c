#include "common.h"

s32 func_L02_004E3D10();
s32 func_L02_004E3FB0();
extern s32 D_0023C1F0_[];
#define D_0023C1F0 (D_0023C1F0_[0])

void func_L02_004E3270(void) {
    if (D_0023C1F0 != 0) {
        if (D_0023C1F0 == 4) {
            func_L02_004E3FB0();
        }
    } else {
        func_L02_004E3D10();
    }
}
