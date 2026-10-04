#include "common.h"

typedef struct Inner {
    char pad0[0xA8];
    s32 fA8;
} Inner;

typedef struct Outer {
    char pad0[0xAC];
    Inner *fAC;
} Outer;

extern Outer *func_L01_004AED78(void);

void func_L01_004AEDB0(void) {
    Outer *o;
    Inner *i;

    o = func_L01_004AED78();
    if (o != NULL) {
        i = o->fAC;
        i->fA8 = i->fA8 + 1;
    }
}
