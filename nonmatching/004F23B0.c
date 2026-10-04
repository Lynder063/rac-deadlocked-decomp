/* Not matching yet (tools/diff_func.py func_004F23B0). Not part of the build. */
#include "common.h"

typedef struct Ring {
    char pad0[4];
    s32 f4;
    s32 f8;
    s32 fC;
    s32 f10;
} Ring;

extern s32 func_004F23A0(void);

s32 func_004F23B0(Ring *r) {
    s32 d;

    if (func_004F23A0() != 0) {
        return 0;
    }
    d = r->f10;
    return r->f4 + ((r->f8 - r->fC + d) % d) * 0x27E40;
}
