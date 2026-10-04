/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497980(s32);
s32 func_0049B2F8(s32, s32);
s32 func_00505B20();

void func_004B6B50(void *a0) {
    if (a0 != NULL) {
        func_0049B2F8(func_00505B20(), 5);
        return;
    }
    func_00497980(5);
    func_0049B2F8(func_00505B20(), -1);
}
