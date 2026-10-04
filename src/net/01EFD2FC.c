/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_01EEDCD0(void *, void *, s32);
s32 func_01EFB760();
extern s32 D_0019D798_[];
#define D_0019D798 (D_0019D798_[0])

void func_01EFD2FC(void *a0) {
    func_01EFB760();
    func_01EEDCD0(a0 + 0x38, &D_0019D798, 0x40);
}
