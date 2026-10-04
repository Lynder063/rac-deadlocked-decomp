#!/usr/bin/env bash
# Fetch the newlib snapshot the math library is built from (2000-02-17) into
# private/newlib. Only its headers are needed to rebuild src/libm; the sources
# that match retail are already in src/libm. Uses anonymous HTTPS from sourceware.
set -euo pipefail
cd "$(dirname "$0")/.."
SNAPSHOT=8a0efa53e44919bcf5ccb1d3353618a82afdf8bc   # "import newlib-2000-02-17 snapshot"
if [ ! -d private/newlib/.git ]; then
    GIT_TERMINAL_PROMPT=0 git clone --filter=blob:none --no-checkout \
        https://sourceware.org/git/newlib-cygwin.git private/newlib
fi
cd private/newlib
GIT_TERMINAL_PROMPT=0 git checkout "$SNAPSHOT" -- newlib/libm newlib/libc/include
mkdir -p ../include
[ -f ../include/stddef.h ] || cat > ../include/stddef.h <<'EOH'
#ifndef _STDDEF_H
#define _STDDEF_H
typedef unsigned int size_t;
typedef int ptrdiff_t;
typedef int wchar_t;
#ifndef NULL
#define NULL ((void *)0)
#endif
#define offsetof(t, m) ((size_t)&((t *)0)->m)
#endif
EOH
echo "newlib snapshot ready in private/newlib"
