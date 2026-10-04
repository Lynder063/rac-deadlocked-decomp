/* cflags: -mno-split-addresses */
#include "common.h"

extern s32 D_0021E814_[];
extern s32 D_0021DDB4_[];
#define D_0021E814 (D_0021E814_[0])
#define D_0021DDB4 (D_0021DDB4_[0])

s32 func_L01_00631CB8(void) {
    s32 r;

    r = 0;
    if (D_0021E814 == 2 || D_0021DDB4 == 2) {
        r = 1;
    }
    return r;
}
