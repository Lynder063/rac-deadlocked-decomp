/* Not matching yet (tools/diff_func.py func_004B79F8). Not part of the build. */
#include "common.h"

typedef struct Flags {
    char pad0[4];
    s8 f4;
    s8 f5;
} Flags;

/* Declared without a size so they are addressed with lui, not $gp (-G8). */
extern Flags D_00171D38[];
extern s32 *D_0021DDA4[];
#define D_0021DDA4 (D_0021DDA4[0])
extern void func_004B5D68(s32 i);

void func_004B79F8(void) {
    s32 i;
    s8 t;

    t = D_00171D38[0].f4 == 0;
    D_00171D38[0].f4 = t;
    D_00171D38[0].f5 = t;
    i = 0;
    if (*D_0021DDA4 > 0) {
        do {
            func_004B5D68(i);
            i += 1;
        } while (i < *D_0021DDA4);
    }
}
