/* Not matching yet (see tools/diff_func.py func_004C8388). Not part of the build. */
#include "common.h"

extern void func_00497980(s32 a);
extern void func_004C8418(void);
extern void func_004E19D8(s32 a, s32 b);

void func_004C8388(void) {
    func_004C8418();
    func_00497980(6);
    func_004E19D8(0x1E, 0);
}
