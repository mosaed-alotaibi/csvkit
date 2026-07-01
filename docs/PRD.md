# PRD — csvkit

**Status:** Living — reflects the as-built v1 system on branch `codex/csv2json`.
**Last updated:** 2026-07-01
**Owner:** mosalotaibi

> This is the canonical record of what csvkit does today. Planned additions live in
> [`BACKLOG.md`](BACKLOG.md); the active cursor lives in
> [`NEXT-STEPS.md`](NEXT-STEPS.md).

## 1. TL;DR

csvkit is a zero-dependency Python 3 command-line tool that converts a header-bearing
CSV file into a JSON array of objects. A user runs
`python3 -m csvkit csv2json <input.csv>` and receives compact JSON on stdout, or uses
`--pretty` and `-o/--output` for formatted/file output. It uses only Python's standard
library and rejects inputs that would otherwise silently lose data.

## 2. Users and problem

The primary user is a developer or operator who needs a deterministic CSV→JSON
conversion without installing a package or writing one-off parsing code. v1 targets a
single local user and one file per invocation; it has no server, datastore, network, or
authentication surface.

## 3. Goals

| ID | Goal | Status |
|---|---|---|
| G1 | Convert ordinary RFC-4180-style CSV into JSON predictably | ✅ built |
| G2 | Fail loudly rather than silently losing data on malformed structure | ✅ built |
| G3 | Remain install-free and third-party-dependency-free | ✅ built |

## 4. Architecture (as built)

```text
python3 -m csvkit
        │
        ▼
csvkit/__main__.py ── delegates to cli.main()
        │
        ▼
csvkit/cli.py ── argparse + filesystem I/O + JSON serialization + error messages
        │
        ▼
csvkit/convert.py ── csv.reader + structural validation → list[dict[str, str]]
```

The module seam is deliberate: `csv_to_json_rows(fileobj)` owns pure conversion;
`cli.main(argv)` owns paths, encoding/newline handling, stdout/files, and exit codes.
See [`STACK_WIRING.md`](STACK_WIRING.md) for the exact contract.

## 5. Functional requirements (as built)

- **FR1 — Module CLI** (`csvkit/__main__.py`, `csvkit/cli.py:main`):
  `python3 -m csvkit csv2json INPUT` is the supported invocation. A missing or invalid
  subcommand is an argparse usage error (exit 2), never a traceback.
- **FR2 — Compact stdout** (`csvkit/cli.py:main`): by default, writes a JSON array with
  no separator spaces and literal UTF-8 text, followed by one newline.
- **FR3 — Pretty output** (`csvkit/cli.py:build_parser`, `main`): `--pretty` uses
  two-space indentation.
- **FR4 — File output** (`csvkit/cli.py:main`): `-o/--output PATH` writes JSON to that
  UTF-8 file and leaves stdout empty.
- **FR5 — CSV parsing** (`csvkit/convert.py:csv_to_json_rows`): supports quoted commas,
  embedded newlines, and doubled quotes through stdlib `csv.reader`.
- **FR6 — Structural validation** (`csvkit/convert.py`): rejects a missing/blank
  header, duplicate columns, and short/long rows with clean, data-row-numbered errors;
  blank data lines are skipped.
- **FR7 — Encoding/newline correctness** (`csvkit/cli.py:main`): opens inputs with
  `encoding="utf-8-sig", newline=""`, stripping an optional BOM and preserving embedded
  CRLF byte semantics.
- **FR8 — Failure translation** (`csvkit/cli.py:main`): conversion, decoding, CSV, and
  filesystem failures produce a one-line stderr message and exit 1. Early-closed pipes
  exit quietly without interpreter-shutdown noise.

## 6. Non-functional requirements

| ID | Requirement | Evidence / status |
|---|---|---|
| NFR1 | Python 3 standard library only | ✅ no third-party imports or dependency manifest |
| NFR2 | Deterministic behavior | ✅ exact stdout/stderr/exit-code tests |
| NFR3 | Portable test command | ✅ `python3 -m unittest discover -s tests -v` |
| NFR4 | No raw traceback for documented user errors | ✅ CLI tests assert clean stderr |

## 7. Verification evidence

The test suite contains **38 passing tests**: 13 package/conversion tests and 25 CLI
surface tests. The CLI has also been driven live against a real CSV for compact stdout,
pretty `-o` output, a missing-file failure, and small-output broken-pipe handling.

Run:

```sh
python3 -m unittest discover -s tests -v
```

## 8. Deferred capabilities

| Backlog ID | Capability |
|---|---|
| BL-001 | JSON→CSV (`json2csv`) |
| BL-002 | Opt-in type inference |
| BL-003 | Custom delimiters |
| BL-004 | Headerless input mode |
| BL-005 | Installable packaging / console script |

## 9. Non-goals

Streaming large files, stdin input, remote URLs, schema validation, automatic type
inference, custom delimiters, and packaging are not part of v1.
