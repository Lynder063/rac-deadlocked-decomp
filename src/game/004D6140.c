/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00498CF8();
s32 func_0049B2F8(s32, s32);
s32 func_00505B20();
extern s8 D_0021FC11_[];
#define D_0021FC11 (D_0021FC11_[0])

void func_004D6140(void) {
    D_0021FC11 = 0;
    func_00498CF8();
    func_0049B2F8(func_00505B20(), -1);
}
