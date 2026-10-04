/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_L00_007758F8(u8 *);
s32 func_L00_00775FF0();

s32 func_L00_007758B8(u8 *arg0) {
    if (*arg0 != 0) {
        func_L00_00775FF0();
        func_L00_007758F8(arg0);
    }
    return 1;
}
