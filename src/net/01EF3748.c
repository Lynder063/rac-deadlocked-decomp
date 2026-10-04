/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_01EEE13C();
s32 func_01EF0550(s32, void *);
s32 func_01EF3CF0();

void func_01EF3748(void *a0) {
    func_01EF3CF0();
    func_01EF0550(func_01EEE13C(), a0);
}
