/* Not matching yet (tools/diff_func.py func_004B9BB0). Not part of the build. */
#include "common.h"

typedef struct Slot14 {
    s32 state;
    char pad[0x10];
} Slot14;

extern Slot14 D_0030A490[];
extern void func_00497980(s32 a, s32 b);

void func_004B9BB0(s32 i) {
    D_0030A490[i].state = 2;
    func_00497980(0xC, 2);
}
