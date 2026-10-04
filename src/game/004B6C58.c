/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497980(s32);
s32 func_0049B208(s32);
s32 func_0049B2F8(s32, s32);
s32 func_00505B20();

void func_004B6C58(void *a0) {
    if (a0 != NULL) {
        func_0049B2F8(func_00505B20(), 5);
        return;
    }
    func_00497980(8);
    func_0049B208(func_00505B20());
}
