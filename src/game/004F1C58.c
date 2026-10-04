#include "common.h"

extern void func_00142140(s32 a);
extern void func_004F1618(s32 a);

s32 func_004F1C58(s32 a) {
    func_004F1618(a + 0x48);
    func_00142140(a);
    return 1;
}
