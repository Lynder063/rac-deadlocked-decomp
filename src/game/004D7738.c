/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004983E8(s32);
s32 func_004D77B8();
s32 func_004D77E0();
s32 func_004D7810();

void func_004D7738(void) {
    s32 temp_v0;

    temp_v0 = func_004983E8(6);
    switch (temp_v0) {
    case 2:
        func_004D77B8();
        return;
    case 4:
        func_004D7810();
        break;
    case 13:
        func_004D77E0();
        break;
    }
}
