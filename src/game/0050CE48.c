#include "common.h"

s32 func_0050CE48(char *p, u32 mask) {
    return (*(u8 *)(p + 0x1EC) & mask) != 0;
}
