/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497980(s32);
s32 func_004BB958();

void func_004BB920(void *a0) {
    if (a0 != NULL) {
        func_00497980(0xE);
        func_004BB958();
        return;
    }
    func_00497980(0xC);
}
