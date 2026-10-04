#include "common.h"

typedef struct Inner {
    char pad0[0xF4];
    u8 fF4;
} Inner;

typedef struct Outer {
    char pad0[0xAC];
    Inner *fAC;
} Outer;

extern void func_L01_00591BD8(void *a, s32 b, s32 c);

void func_L01_004E4DC8(Outer *o) {
    o->fAC->fF4 = 0;
    func_L01_00591BD8(o, 1, -1);
}
