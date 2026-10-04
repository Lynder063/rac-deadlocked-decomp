/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004EF3E0();
s32 func_004F1010(s32);
extern s32 D_221ED4_[];
#define D_221ED4 (D_221ED4_[0])

s32 func_004F2070(s32 a0, s32 a1, s32 a2) {
    func_004EF3E0();
    func_004F1010(D_221ED4 + 0x48);
    return 1;
}
