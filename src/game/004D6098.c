/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_004983E8(s32 a0);
void func_0049B208(s32 a0);
void func_004D6140(void);
void func_004D6178(s32 a0);
s32 func_00505B20(void);

void func_004D6098(void) {
    s32 temp_s0;
    s32 temp_v0;
    s32 var_s1;

    var_s1 = 0;
    temp_s0 = func_00505B20();
    temp_v0 = func_004983E8(6);
    switch (temp_v0) {
    case 2:
        func_0049B208(temp_s0);
        return;
    case 5:
        var_s1 = 1;
        /* fallthrough */
    case 6:
        func_004D6178(var_s1);
        break;
    case 13:
        func_004D6140();
        break;
    }
}
