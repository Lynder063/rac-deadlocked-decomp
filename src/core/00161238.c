#include "common.h"

s32 func_00161168(s32, s32, s32);
extern s8 D_00173A30_[];
#define D_00173A30 (D_00173A30_[0])

s32 func_00161238(s32 a0) {
    if (func_00161168(1, 0xA, a0) == 0) {
        D_00173A30 = 1;
    }
    return 0;
}
