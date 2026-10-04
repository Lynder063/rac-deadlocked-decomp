#include "common.h"

extern s16 D_001DFC4C[];
#define D_001DFC4C (D_001DFC4C[0])
extern void func_004F3538(void);
extern void func_004F5008(void);
extern void func_004F5868(void);

void func_004F6250(void) {
    func_004F5008();
    func_004F3538();
    func_004F5868();
    D_001DFC4C = 1;
}
