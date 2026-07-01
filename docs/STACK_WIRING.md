# Stack Wiring & Swap Guide — csvkit

**As-built, verified against the live code on 2026-07-01.**

## 1. Request chain

```text
shell
  └─▶ csvkit/__main__.py
        └─▶ csvkit.cli.main(argv)
              ├─▶ open(INPUT, encoding="utf-8-sig", newline="")
              ├─▶ csvkit.convert.csv_to_json_rows(fileobj)
              │     └─▶ csv.reader(fileobj)
              └─▶ json.dumps(...) ──▶ stdout or UTF-8 OUTPUT file
```

## 2. The contracts

1. **Entrypoint contract** — `csvkit/__main__.py` exits with `cli.main()`'s integer
   result. Argparse usage errors exit 2 before conversion starts.
2. **Conversion seam** — `csv_to_json_rows(fileobj)` accepts an already-open text
   stream and returns `list[dict[str, str]]`; it owns CSV structure, not files or stderr.
3. **I/O seam** — `cli.main(argv)` owns path opening, BOM/newline semantics, JSON
   formatting, output destination, one-line errors, and process exit codes.
4. **Error seam** — conversion errors carry detail through exception text; the CLI adds
   `csv2json: PATH:`. Filesystem errors use `OSError.strerror` and an input/output/stdout
   phase discriminator.

## 3. Swappable components

| Component | Current implementation | Safe-swap condition |
|---|---|---|
| CSV parser | stdlib `csv.reader` | Preserve quoted-field semantics and all validation/error contracts |
| JSON serializer | stdlib `json.dumps` | Preserve compact/pretty bytes and literal UTF-8 behavior |
| CLI parser | stdlib `argparse` | Preserve documented help text, flags, and exit 2 usage errors |

## 4. Load-bearing details

- `newline=""` is required; otherwise embedded CRLF is rewritten before `csv.reader`
  sees it.
- `encoding="utf-8-sig"` strips a common Excel-export BOM without changing ordinary
  UTF-8 input.
- `sys.stdout.flush()` must remain inside the guarded write path; otherwise a small
  broken-pipe failure can surface only at interpreter shutdown as exit 120 plus noise.
- `BrokenPipeError` must be handled before its parent `OSError`.
- The OSError prefix is selected by phase (`reading_done`) plus whether `-o` was given,
  never by comparing input/output path strings.

## 5. Verification after any swap

```sh
python3 -m unittest discover -s tests -v
```

Then live-run compact stdout, pretty `-o`, one input failure, and a closed-pipe case.
