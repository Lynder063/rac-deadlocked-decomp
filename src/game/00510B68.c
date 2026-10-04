#include "common.h"

typedef struct Pool {
    char pad0[0x14];
    s32 count;
    void *freeList;
} Pool;

void func_00510B68(Pool *pool, void **node) {
    if (node != NULL) {
        *node = pool->freeList;
        pool->freeList = node;
        pool->count = pool->count - 1;
    }
}
