#include "common.h"

typedef struct Table {
    char pad0[0x14];
    s32 index;
} Table;

typedef struct Holder {
    char pad0[4];
    Table *table;
} Holder;

extern void func_005005D8(s32 v);

void func_00500ED0(Holder *h) {
    Table *t = h->table;
    func_005005D8(*(s32 *)((u32)t + (t->index << 2)));
}
