#include "common.h"

u32 func_00139A58(u32 a) {
    if (a >> 28 == 7) {
        a = a & 0xFFFFFFF;
        a = a | 0x80000000;
    }
    return a;
}
