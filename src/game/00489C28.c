/* cflags: -mno-split-addresses */
#include "common.h"

s32 func_00157F98(void);
void func_001634A8(u32 a0);
u32 func_00163928(void);
void func_00489740(void);

s32 func_00489C28(s32 a0) {
    func_001634A8((u32) a0);
    do {

    } while (func_00157F98() != 0);
    func_00489740();
    do {

    } while (func_00157F98() != 0);
    return func_00163928();
}
