#include "common.h"

typedef struct Obj {
    char pad0[0x20];
    u8 state;
    char pad21[0x47];
    u8 prevState;
    u8 stateType;
    u16 stateTimer;
    char pad6C[0x52];
    u8 flags;
} Obj;

void func_00473A88(Obj *o, u8 state, s32 type) {
    u8 flags = o->flags & 0xFE;
    u8 prev = o->state;
    o->state = state;
    o->prevState = prev;
    o->stateTimer = 0;
    o->flags = flags;
    if (type != -1) {
        o->stateType = type;
        o->flags = flags & 0xFD;
    }
}
