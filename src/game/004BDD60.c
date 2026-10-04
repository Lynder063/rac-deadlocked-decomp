/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00497980(s32);
s32 func_004BDDF8();

void func_004BDD60(void *a0) {
    if (a0 != NULL) {
        func_004BDDF8();
        return;
    }
    func_00497980(0xC);
}
