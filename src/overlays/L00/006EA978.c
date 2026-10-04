/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_005DC9A8(s32);
s32 func_L00_005DCC30();

void func_L00_006EA978(s32 arg0) {
    if (func_L00_005DCC30() != 0) {
        func_L00_005DC9A8(arg0);
    }
}
