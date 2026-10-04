/* cflags: -mno-split-addresses */
#include "common.h"

extern s32 D_00221ED8[];
#define D_00221ED8 (D_00221ED8[0])
extern void func_004EFA68(s32 a);

void func_004EF6A8(void) {
    func_004EFA68(D_00221ED8);
}
