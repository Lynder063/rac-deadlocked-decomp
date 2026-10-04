#include "common.h"

typedef struct Rec20 {
    char pad0[0x1C];
    s32 f1C;
} Rec20;

extern Rec20 D_00326A60[];

void func_004EA8B0(s32 i) {
    if (i >= 0) {
        Rec20 *r = D_00326A60 + i;
        r->f1C = 0;
    }
}
