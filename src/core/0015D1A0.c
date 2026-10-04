#include "common.h"

/* Declared without a size so the compiler addresses them with lui/lw, not $gp (-G8). */
extern void (*D_00212038[])(void);
extern void (*D_00212090[])(void);
#define D_00212038 (D_00212038[0])
#define D_00212090 (D_00212090[0])

void func_0015D1A0(void) {
    if (D_00212038) {
        D_00212038();
    }
}

void func_0015D470(void) {
    if (D_00212090) {
        D_00212090();
    }
}
