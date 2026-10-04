#include "common.h"

s32 func_L00_00764250();
extern s32 D_004EE5B8_[];
#define D_004EE5B8 (D_004EE5B8_[0])

s32 *func_L00_007642F8(void) {
    if (D_004EE5B8 == 0) {
        func_L00_00764250();
    }
    return &D_004EE5B8;
}
