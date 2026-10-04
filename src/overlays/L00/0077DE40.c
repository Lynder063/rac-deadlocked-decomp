#include "common.h"

s32 func_0011A518(s32 *, s32, s32);
extern s32 D_003B1720_[];
#define D_003B1720 (D_003B1720_[0])

void func_L00_0077DE40(s32 arg0) {
    D_003B1720 = 0;
    func_0011A518(&D_003B1720 + 4, 0, 0x14);
    func_0011A518(arg0 + 0xDC, 0, 5);
}
