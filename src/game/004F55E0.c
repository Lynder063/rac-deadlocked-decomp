/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004494E8(s32, s32);
s32 func_004F2728(s32, s32);
extern s32 D_221F40_[];
#define D_221F40 (D_221F40_[0])

s32 func_004F55E0(u32 a0, u32 a1) {
    func_004F2728(0, 0);
    func_004494E8(6, 0);
    D_221F40 = 0x12C;
    return 1;
}
