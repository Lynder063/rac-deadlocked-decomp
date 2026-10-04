/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005BC9B8(s32);
s32 func_L00_00607960(s32);

void func_L00_0060E620(s32 arg0) {
    if (func_L00_005BC9B8(arg0 + 0xA) != 0) {
        func_L00_00607960(arg0);
    }
}
