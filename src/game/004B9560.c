/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004983E8(s32);
s32 func_0049B208(s32);
s32 func_00505B20();

void func_004B9560(void) {
    s32 temp_v0;

    temp_v0 = func_004983E8(6);
    if ((temp_v0 == 1) || (temp_v0 == 0xD)) {
        func_0049B208(func_00505B20());
    }
}
