/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0011AE00(s32, s32, s32);

s32 func_L00_00770C70(s32 arg0, s32 arg1) {
    if ((arg0 != 0) && (arg1 != 0)) {
        return func_0011AE00(arg0 + 0x60, arg1 + 0x60, 0x40) > 0;
    }
    return 0;
}
