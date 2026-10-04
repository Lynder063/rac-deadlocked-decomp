#include "common.h"

typedef struct Obj {
    char pad0[0x30];
    u8 f30;
    char pad34[0x78];
    s32 fAC;
} Obj;

extern void func_L00_005DD4A0(Obj *o);
extern s32 func_L01_00568EF0(s32 a);

void func_L01_003EE8F0(Obj *o) {
    o->f30 = 0xFF;
    if (func_L01_00568EF0(o->fAC) == 0) {
        func_L00_005DD4A0(o);
    }
}
