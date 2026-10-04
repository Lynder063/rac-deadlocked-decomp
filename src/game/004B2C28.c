#include "common.h"

extern char D_0021F7B8[];
extern void func_0011D920(void *dst, void *fmt, s32 v);

void func_004B2C28(s32 *p) {
    func_0011D920(p + 8, D_0021F7B8, *p);
}
