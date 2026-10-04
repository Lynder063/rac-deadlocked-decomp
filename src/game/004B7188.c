/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_0045C6E8();
s32 func_00497980(s32);
s32 func_00497EB8(s32, s32);
s32 func_00505B20();

void func_004B7188(void *a0) {
    if (a0 != NULL) {
        func_00497EB8(func_00505B20(), 0);
        func_0045C6E8();
        return;
    }
    func_00497980(0xC);
}
