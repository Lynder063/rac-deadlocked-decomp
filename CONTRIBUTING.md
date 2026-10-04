## Contributing

The workflow follows [rac1-decomp](https://github.com/Lynder63/rac1-decomp)
and will be documented in `docs/WORKFLOW.md` as the build comes together.

1. Pick a function.
2. Get a starting point with [m2c](https://github.com/matt-kempster/m2c).
3. Put the C in `src/`, named `func_XXXXXXXX` after the address in `asm/`.
   Build with `bash tools/docker/run.sh bash tools/build.sh` and compare with
   `venv/bin/python tools/audit_matches.py`.
4. Regenerate the progress report with `python tools/gen_progress_report.py`
   and commit it with your change. CI fails if the report disagrees with `src/`.

```
git clone https://github.com/matt-kempster/m2c tools/ext/m2c
git clone https://github.com/simonlindholm/asm-differ tools/ext/asm-differ
```

## Sources

Read [`LEGAL.md`](LEGAL.md). Never use Sony SDK source, samples or headers, or
leaked or NDA material, not even as a reference to check a match against.
