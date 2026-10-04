#include "common.h"

typedef struct Vec3Obj {
    f32 f0;
    f32 f4;
    f32 f8;
    s32 fC[4];
    u8 f1C;
} Vec3Obj;

s32 func_L01_00573B80(Vec3Obj *o, f32 x, f32 y, f32 z) {
    s32 *p;
    s32 i;

    o->f0 = x;
    i = 3;
    o->f4 = y;
    p = o->fC;
    o->f8 = z;
    do {
        *p = 0;
        i -= 1;
        p += 1;
    } while (i >= 0);
    o->f1C = 1;
    return 1;
}
