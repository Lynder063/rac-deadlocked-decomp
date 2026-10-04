#include "common.h"

typedef struct Rec54 {
    char pad0[0x14];
    s32 f14;
    s32 f18;
    char pad1C[0x38];
} Rec54;

extern Rec54 D_002F32B8[];

void func_00497438(s32 i, s32 a, s32 b) {
    Rec54 *r = D_002F32B8 + i;
    r->f14 = a;
    r->f18 = b;
}
