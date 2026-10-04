#include "common.h"

void func_004E2488(s32 unused, volatile char *p) {
    p[0x10] = 0;
    *(volatile s32 *)(p + 0x1C) = 0;
    *(volatile s32 *)(p + 0x40) = 0;
}
