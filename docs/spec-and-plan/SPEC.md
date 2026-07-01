# csv2json (v1) — Design Spec

**Date:** 2026-07-01 · **Branch:** `main` (off `main`) · **Status:** spec (decisions settled, implementation-ready)
**Scope owner surface:** `csvkit/` (package code), `tests/` (test suite)
**Hub file(s):** none — this is the first feature; no shared hub exists yet.

---

## 1. Summary, scope & non-goals

`csvkit` ships its first command: `csv2json`. It reads a CSV file (first row = header)
and writes a JSON array of objects to stdout or a file, using Python's stdlib `csv`
module for RFC 4180 parsing. All values stay JSON strings in v1 — no type inference.

**In scope:**
- `python3 -m csvkit csv2json <input.csv>` — read a CSV file, print JSON array to stdout.
- `-o/--output <path>` — write to a file instead of stdout.
- `--pretty` — indented (2-space) JSON instead of compact.
- Correct handling of quoted fields, embedded commas, embedded newlines, and escaped
  (doubled) quotes (verified against the installed Python 3.12.13 `csv` module — see §2,
  all four cases individually probed).
- Loud, exact **data-row**-numbered failure on a ragged row (a data row whose field
  count doesn't match the header's). "Data row" means the Nth record `csv.reader`
  yields after the header — **not** the physical file line, which can differ once any
  earlier row contains an embedded newline (see §2).
- Loud failure on duplicate header column names (same silent-data-loss risk as a ragged
  row — see §2's material finding).
- A `-h/--help` usage message.

**Non-goals / explicitly out of scope:**
- JSON → CSV (the reverse direction). A different command, different surface.
- Custom delimiters (semicolon, tab) — v1 is comma-only.
- `--no-header` mode (assume row 1 is always the header).
- Packaging for `pip install` / a `setup.py` or `pyproject.toml` — v1 runs via
  `python3 -m csvkit`, which needs no packaging.

**Deferred (named, with enabler):**
- `json2csv` (the reverse command) → enabled once csv2json ships and a second real
  direction is actually needed (BL-001).
- `--infer-types` (numbers/booleans/null instead of all-strings) → enabled once a
  consumer actually needs typed JSON, not strings (BL-002).
- `--delimiter` (semicolon/tab support) → enabled by a real non-comma input file
  showing up (BL-003).
- `--no-header` mode → enabled by a real headerless input file showing up (BL-004).
- pip-installable packaging (`pyproject.toml`, console-script entry point) → enabled
  once csvkit is used outside this checkout (BL-005).

---

## 2. Context & current state

Greenfield. `csvkit/__init__.py` exists with a module docstring and `__version__ =
"0.1.0"`; no CLI, no conversion logic. `tests/test_package.py` has one smoke test
proving the package imports; no feature tests yet.

**Dependency-reality check (Ritual 16) — Python's `csv` module, verified live against
the installed Python 3.12.13**, not assumed from memory:

```python
>>> csv.DictReader(io.StringIO("a,b,c\n1,2\n"))       # short row
[{'a': '1', 'b': '2', 'c': None}]                      # missing field -> None, SILENT
>>> csv.DictReader(io.StringIO("a,b,c\n1,2,3,4\n"))    # long row
[{'a': '1', 'b': '2', 'c': '3', None: ['4']}]           # extra fields -> None KEY, SILENT
>>> csv.DictReader(io.StringIO('a,b\n"hello, world","line1\nline2"\n'))
[{'a': 'hello, world', 'b': 'line1\nline2'}]            # quoting/embedded newline: correct, no special-casing needed
>>> csv.DictReader(io.StringIO('a,b\n"he said ""hi""","normal"\n'))
[{'a': 'he said "hi"', 'b': 'normal'}]                  # escaped (doubled) quote: correct, no special-casing needed
>>> dict(zip(['a', 'b', 'a'], ['1', '2', '3']))         # duplicate header columns
{'a': '3', 'b': '2'}                                    # value '1' SILENTLY DROPPED — same footgun class as ragged rows
>>> next(csv.reader(io.StringIO("\n")))                 # a file whose first physical line is blank
[]                                                        # NOT StopIteration — header becomes [], width 0 (see §3 decision 7)
```

**Material finding vs. the brief:** `DictReader`'s default leniency on ragged rows would
silently produce a JSON object containing a literal `null` key (Python `None` serializes
to JSON `null`, and `json.dumps` accepts a `None` dict key by coercing it to the string
`"null"` — confirmed below) — a real footgun for any downstream JSON consumer. The same
class of silent-data-loss footgun exists for **duplicate header columns**: `dict(zip(...))`
silently keeps only the *last* value for a repeated key, with no error and no length
mismatch to trigger a ragged-row check. §3 settles both: v1 detects and rejects ragged
rows *and* duplicate headers explicitly, rather than inheriting the stdlib's silent
defaults.

```python
>>> import json; json.dumps({None: ['4'], 'a': '1'})
'{"null": ["4"], "a": "1"}'   # confirms the ragged-row footgun is real if left unguarded
```

**Physical line vs. data-row numbering:** `csv.reader` exposes a `.line_num` attribute
that tracks the true physical file line (verified: for a file where row 2 contains an
embedded newline, `.line_num` correctly reads 3 after consuming it and 4 after the next
row — matching the real file). v1 deliberately does **not** use this — see §3 decision 2
for why a data-row count is the better fit here despite `.line_num` being available.

**File-open gotchas — verified against a REAL file on disk (`io.StringIO` cannot
reproduce either of these; they only manifest through Python's actual text-mode I/O
layer):**

```python
# A real file with CRLF line terminators and a quoted field containing an embedded \r\n:
>>> open(path, encoding="utf-8").read()  # then csv.reader() on it, NO newline=''
[['a', 'b'], ['line1\nline2', 'x']]      # the embedded \r\n was silently rewritten to \n
>>> open(path, encoding="utf-8", newline="").read()  # WITH newline=''
[['a', 'b'], ['line1\r\nline2', 'x']]    # exact bytes preserved, as the csv module intends

# A real UTF-8 file with a leading byte-order mark (BOM) — a common "CSV UTF-8" export
# from Excel:
>>> open(path, encoding="utf-8").readline()
'﻿a,b\n'                             # BOM survives as part of the first header name
>>> open(path, encoding="utf-8-sig").readline()
'a,b\n'                                   # utf-8-sig strips a leading BOM if present, no-op otherwise
```

Python's own `csv` module documentation states files should always be opened with
`newline=''` for exactly this reason — confirmed empirically above, not just cited.

---

## 3. Settled decisions / forks

| # | Fork / question | Decision (rationale) |
|---|---|---|
| 1 | Use the stdlib `csv` module vs. a hand-rolled parser? And within the stdlib, `csv.reader` or `csv.DictReader`? | **Stdlib, via bare `csv.reader`** (not `DictReader`). Verified (§2) the stdlib correctly handles RFC 4180 quoting, embedded commas/newlines, and escaped quotes — no reason to reimplement a battle-tested parser. `DictReader` is deliberately **not** used: it builds the row `dict` before ragged-row or duplicate-header checks can run (§3 decisions 2, 8), which is precisely how it silently produces the `None`-keyed footgun documented in §2 — `csv.reader` lets §4.3 validate *before* building the dict. |
| 2 | Ragged rows (field count ≠ header count): accept `DictReader`'s lenient default, or reject? Report the failing **data row** (record count) or the **physical file line**? | **Reject, loudly**, reporting the 1-indexed **data-row** number (not physical line), with a non-zero exit code. Rationale for rejecting: `DictReader`'s default silently produces a `None`-keyed JSON object (verified §2) — accepting that is exactly the kind of latent risk Keelwright's "harden, don't defer" principle says to close now, not file for later. Rationale for data-row over physical line (`.line_num`, verified available in §2): a user thinking about "row 7 of my CSV" almost always means the 7th record, matching how a spreadsheet app would show it — not the 9th physical file line after two earlier multi-line quoted fields shifted the count. Data-row numbering is also simpler to implement and test correctly. |
| 3 | Value typing: infer int/float/bool, or keep everything as JSON strings? | **All strings in v1.** Inference is ambiguous (e.g. a zip code `"02134"` would lose its leading zero if coerced to a number) and reversible later without breaking anything — `--infer-types` is a strict additive opt-in, deferred to BL-002. |
| 4 | Output shape: array-of-objects, or object-keyed-by-some-column? | **Array of objects** (`[{...}, {...}]`) — the unambiguous, universally-expected shape for "a CSV as JSON"; a keyed shape would need a designated key column, which is unscoped complexity for v1. |
| 5 | CLI invocation shape: a real `pip`-installed console script, or `python3 -m csvkit`? | **`python3 -m csvkit`** — zero packaging, zero install step, matches the stdlib-only, no-dependencies rule locked in `docs/PROJECT_RULES.md` → Project-specific conventions → Environment / stack conventions. Packaging is deferred (BL-005) until there's a real reason to install it outside this checkout. |
| 6 | Empty input (header-only, or a genuinely empty file)? | **Header-only → `[]`** (valid, zero data rows). **Genuinely empty file (no header) → a loud error** ("empty input: no header row"), not a silent `[]`, since a caller who passed an empty file almost certainly made a mistake and an empty-but-plausible `[]` output would hide that. |
| 7 | A file whose first physical line is blank (`next(csv.reader(...))` returns `[]`, not `StopIteration` — verified §2): treat as a 0-column header, or as the same "empty input" error as #6? | **Same as #6 — a loud "empty input" error.** A blank first line is never a legitimate header; falling through to width-0 ragged-row comparisons (as the naive `StopIteration`-only check would) produces a confusing `"expected 0 fields, got N"` message instead of a clear one. Detected by checking `width == 0` right after reading the header, not just catching `StopIteration`. |
| 8 | Duplicate header column names (e.g. `a,b,a`): accept `dict(zip(...))`'s silent last-value-wins default, or reject? | **Reject, loudly**, naming the offending column, mirroring decision #2's ragged-row treatment. Rationale: verified in §2 that a duplicate header silently drops every value but the last for that column, with **no length mismatch** to trigger the ragged-row check — an equally real, equally silent footgun for a downstream JSON consumer, and one that decision #2's hardening does not happen to catch as a side effect. |
| 9 | How to `open()` the input file: plain defaults, or with explicit `newline=`/`encoding=` handling? | **`open(path, encoding="utf-8-sig", newline="")`.** Rationale, both verified live in §2 on a real file (not `io.StringIO`, which can't reproduce either bug): (a) `newline=""` is required because Python's text-mode universal-newline translation otherwise silently rewrites an embedded `\r\n` inside a quoted field to `\n` on CRLF-terminated files — exactly the RFC 4180 terminator this spec claims to support, and exactly what Excel/Windows commonly produce; (b) `utf-8-sig` (not plain `utf-8`) is required because a leading UTF-8 BOM — common in Excel's "CSV UTF-8" export — is valid UTF-8 and raises no error, but silently prepends an invisible character to the first header name unless stripped. |
| 10 | How to catch filesystem-level errors: enumerate every specific `OSError` subclass (`FileNotFoundError`, `IsADirectoryError`, …), or one blanket `except OSError`? | **One blanket `except OSError as e:`**, formatted via `e.strerror`. Rationale: enumeration is an open-ended, ever-incomplete list — verified live that `PermissionError` (a `chmod 000` input file) and `NotADirectoryError` (an `-o` path with a file, not a directory, as a path component) are both real, distinct `OSError` subclasses that an itemized catch list already missed twice in this spec's own review cadence (rounds 1 and 3). `OSError.strerror` naturally produces a distinct, human-readable message per underlying failure ("No such file or directory", "Is a directory", "Permission denied", "Not a directory", …) without the design needing to name every subclass in advance. |
| 11 | JSON output encoding: default `json.dumps` (`ensure_ascii=True`, escapes non-ASCII to `\uXXXX`), or `ensure_ascii=False` (literal UTF-8 text)? | **`ensure_ascii=False`.** A CSV cell containing non-ASCII text (e.g. an accented name) should round-trip as literal UTF-8 in the JSON output, consistent with the effort already spent (§3 decision 9) getting UTF-8/BOM input handling right — escaping to `\uXXXX` would be valid JSON but pointlessly harder to read, and there is no compatibility reason to prefer it for v1 (no legacy ASCII-only consumer is in scope). |
| 12 | A blank data row (`csv.reader` yields `[]` — verified §2 this isn't unique to the header position): treat as a ragged row (`0 != width`), or skip it? | **Skip it silently** — no object appended to the output, data-row counting for later error messages continues via the same `enumerate` index regardless (so "row N" in a later ragged-row message still means the Nth row read from the file, blank rows included, matching how a human would count while scrolling the file). Rationale: verified live that a trailing blank line — an extremely common real-world shape (an editor's "insert final newline" plus one extra Enter, or `cat`-concatenating two files) — was being misclassified as a ragged row by decision #2's own check, which is backwards: decision #2 rejects ragged rows because they risk *silent data loss*, but a blank line loses nothing, so rejecting it serves no one. **Caveat (single-column CSVs only):** for a width-1 header, this is genuinely ambiguous with a legitimate empty-value record — verified `csv_to_json_rows` on `"a\n\n1\n"` returns `[{"a": "1"}]`, silently dropping what could have been an intended `{"a": ""}` row. Accepted for v1, matching common tooling convention (e.g. pandas' default `skip_blank_lines=True` has the same limitation) — a caller needing an explicit empty value in a single-column CSV must write it as `""`, not a bare blank line. |
| 13 | The single `except OSError` clause (decision 10) must pick one of two message prefixes (`csv2json: <path>: …` for input-side, `csv2json: cannot write <path>: …` for `-o`-side) — by what signal? | **An explicit phase flag**, not filename comparison. `cli.py` sets `reading_done = True` immediately after `convert.csv_to_json_rows` returns successfully; the `except OSError` block uses the input-side prefix if `not reading_done`, else the `-o`-side prefix. Rationale: comparing `e.filename == args.output` breaks when the input and `-o` paths are the same string (e.g. `-o missing.csv` reusing the input path) — verified live this misattributes an input-read failure to the write side, sending a debugging user to the wrong place. A phase flag is correct regardless of whether the two paths happen to collide. |
| 14 | `csv.reader` can itself raise `csv.Error` (e.g. "field larger than field limit" on an oversized quoted field — the stdlib's default limit is 131072 bytes) — is this caught by any of decisions 10's five clauses? | **No — verified live it is not** (`csv.Error`'s only base is `Exception`; it is not a `ValueError`, not `OSError`, not `UnicodeDecodeError`). It needs its **own**, sixth, `except` clause in `cli.py` (§4.1 updated from "five" to "six"). v1 keeps the stdlib's default field-size limit rather than calling `csv.field_size_limit()` to raise it — 128KB is generous for ordinary CSV cells, and raising an arbitrary, unbounded limit trades one risk (a legitimate large cell gets rejected) for another (a malicious/malformed file exhausts memory), which is unscoped complexity for v1 (YAGNI); the failure is caught and reported cleanly either way. |
| 15 | The top-level `python3 -m csvkit` parser's `add_subparsers`: default (subcommand optional), or `required=True`? | **`required=True`.** Verified live that the default (no `required=True`) lets a bare `python3 -m csvkit`, with no subcommand, fall through to `cli.main()`'s body and crash on a missing `args.input` attribute with a raw `AttributeError` traceback — a direct violation of the "never a raw traceback" guarantee, on literally the first command shape a new user might try (running the module with no arguments to see what happens). `required=True` makes `argparse` itself print usage and exit cleanly instead. |
| 16 | Decision 13's phase flag only distinguishes "reading" vs. "writing to `-o`" — but a **third** case exists: writing to **stdout** (no `-o` given) can also fail, most commonly `BrokenPipeError` when the output is piped into a truncating consumer (`\| head`, `\| less`, `\| grep -m1` — an entirely ordinary way to explore a CLI's output). What should happen? | **Two-part decision**, verified live (built the exact mechanism, piped into `head`): (a) **`BrokenPipeError` gets its own, dedicated `except` clause**, ordered before the generic `OSError` clause (Python requires more-specific exceptions listed first; `BrokenPipeError` is itself an `OSError` subclass). It is **not a user-facing error** — the downstream reader closing early is the *reader's* choice, not a real failure — so `csvkit` follows [Python's own documented SIGPIPE idiom](https://docs.python.org/3/library/signal.html#note-on-sigpipe): redirect `stdout` to `os.devnull` (suppresses Python's own noisy "Exception ignored" message on interpreter shutdown) and exit 1 with **no stderr message** — verified this produces empty stderr, not a traceback. (b) Any **other** stdout-write failure (rare — e.g. a full disk when redirected to a file, `csv2json big.csv > /full/disk`) is a genuine failure and gets a **path-less** message, since stdout has no path: `csv2json: error writing output: {e.strerror}`. The existing `-o`-side message (`cannot write {args.output}: …`) now applies only when `args.output is not None` — the three cases (input / `-o` / stdout) are distinguished by `reading_done` plus whether `args.output` is `None`, not by the two-state flag alone. |

---

## 4. Design

### 4.1 Module layout

- `csvkit/__init__.py` — package marker, `__version__` (exists).
- `csvkit/convert.py` — the pure conversion logic: `csv_to_json_rows(fileobj) -> list[dict]`,
  plus the exception classes it raises: `EmptyInputError`, `DuplicateHeaderError`,
  `RaggedRowError` (all defined here, §4.2). Takes a file-like object, not a path — keeps
  it testable in-memory without touching disk, and reusable if the module is imported
  elsewhere later.
- `csvkit/cli.py` — argument parsing (`argparse`, stdlib) and I/O glue: opens the input
  path with `open(path, encoding="utf-8-sig", newline="")` (§3 decision 9 — both
  arguments are load-bearing, not defaults), calls `convert.csv_to_json_rows`, sets a
  local `reading_done = True` immediately on that call's success (§3 decision 13),
  serializes with `json.dumps`, writes to stdout or the `-o` path. Catches and
  translates every failure into a clean one-line stderr message + exit code 1 (never a
  raw traceback). **Seven distinct exception types** need handling (the literal number
  of `except` clauses is an implementation choice, not dictated here — `EmptyInputError`,
  `DuplicateHeaderError`, `RaggedRowError`, and `csv.Error` all resolve to the same
  message shape and may share one clause; `UnicodeDecodeError`, `BrokenPipeError`, and
  `OSError` each need distinct handling and must be tried in that relative order, since
  Python requires the more-specific `BrokenPipeError` before its parent `OSError`):
  `EmptyInputError`, `DuplicateHeaderError`, `RaggedRowError` (the three `convert.py`
  `ValueError` subclasses, §4.2, each formatted `csv2json: {path}: {e}`); `UnicodeDecodeError`
  (verified: a `UnicodeError`/`ValueError` subclass, **not** `OSError` — a hardcoded "not
  valid UTF-8" message, not `str(e)`, so it can't share the clause above); `csv.Error`
  (verified: subclasses only `Exception` — not caught by any of the above — §3 decision
  14, same message shape as the first three); `BrokenPipeError` (§3 decision 16 — **not**
  reported as an error; a quiet exit 1, since a downstream reader closing the pipe early,
  e.g. `csvkit ... \| head`, is the reader's choice, not csvkit's failure); and one
  blanket `except OSError as e:` covering **every remaining** filesystem-level failure —
  a missing file, a directory given where a file was expected, a permission error, a
  path component that isn't a directory, an unwritable `-o` target, a stdout write
  failure that isn't a broken pipe, and anything else `OSError`-derived — formatted via
  `e.strerror`, with `reading_done` and whether `args.output is not None` together
  choosing which of the **three** documented message forms applies (§3 decisions 10,
  13, 16; not enumerated one subclass at a time, and not discriminated by comparing
  paths — both explained in decision 13's rationale).
- `csvkit/__main__.py` — the `python3 -m csvkit` entry point; delegates to `cli.main()`.
  The top-level `argparse` parser uses `add_subparsers(dest="command", required=True)`
  (§3 decision 15) so a bare `python3 -m csvkit` (no subcommand) prints usage and exits
  cleanly — never a raw `AttributeError` traceback from a missing `args.input`.

### 4.2 Exceptions

All three live in `csvkit/convert.py`, all subclass `ValueError` (a malformed-input
signal, distinct from `OSError`'s I/O-failure signal used for file-system errors):

```python
class EmptyInputError(ValueError):
    """Raised when the input has no header row at all (genuinely empty, or a
    blank first line — see §3 decisions 6 and 7)."""
    def __init__(self, message: str = "empty input: no header row"):
        super().__init__(message)


class DuplicateHeaderError(ValueError):
    def __init__(self, column: str):
        self.column = column
        super().__init__(f"duplicate header column: {column!r}")


class RaggedRowError(ValueError):
    def __init__(self, row_number: int, expected: int, got: int):
        self.row_number = row_number
        super().__init__(
            f"row {row_number}: expected {expected} fields, got {got}"
        )
```

`RaggedRowError.row_number` is 1-indexed and counts **data rows only** — the Nth record
`csv.reader` yields after the header (header itself is not counted), matching how a user
would count rows in a spreadsheet viewer. It is **not** the physical file line number
(§3 decision 2 explains why data-row counting was chosen over `csv.reader.line_num`,
which is available but deliberately unused).

### 4.3 `csv_to_json_rows(fileobj) -> list[dict]`

```python
def csv_to_json_rows(fileobj) -> list[dict]:
    reader = csv.reader(fileobj)
    try:
        header = next(reader)
    except StopIteration:
        raise EmptyInputError()
    if len(header) == 0:
        # A blank first physical line does NOT raise StopIteration (verified §2) —
        # csv.reader yields [] instead. Treat it the same as a missing header (§3 #7).
        raise EmptyInputError()

    seen = set()
    for column in header:
        if column in seen:
            raise DuplicateHeaderError(column)
        seen.add(column)

    width = len(header)
    rows = []
    for i, raw_row in enumerate(reader, start=1):
        if len(raw_row) == 0:
            # A blank line in the DATA region (not just the header position — §3 #7
            # only covered the header) also yields [] rather than being skipped by
            # csv.reader (verified §2). Skip it: it loses no data, unlike a genuine
            # ragged row (§3 #12), so treating it as one would be backwards.
            continue
        if len(raw_row) != width:
            raise RaggedRowError(i, width, len(raw_row))
        rows.append(dict(zip(header, raw_row)))
    return rows
```

Uses `csv.reader` (not `DictReader`) precisely so ragged rows are caught **before** a
`dict` is built — `DictReader` would already have silently produced the `None`-keyed
dict by the time code could inspect it (confirmed in §2's probe). The duplicate-header
check runs once, right after the header is read and validated non-empty — before any
data row is processed, so a duplicate-header file fails immediately rather than after
partially converting rows.

**`csv.Error` can propagate from this function** (from either `next(reader)` or the data
loop — e.g. a field exceeding the stdlib's field-size limit, §3 decision 14). This
function deliberately does **not** catch it — `convert.py` stays a pure translation of
CSV structure to Python data; exception-to-stderr-message translation is entirely
`cli.py`'s job (§4.1's sixth `except` clause), same as every other exception this
function raises.

### 4.4 CLI contract

Exact `-h` output — **captured from a real `argparse.ArgumentParser`** configured per
this contract (not hand-typed), so the indentation is byte-accurate:

```
usage: python3 -m csvkit csv2json [-h] [-o OUTPUT] [--pretty] input

positional arguments:
  input                 path to the input CSV file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        write JSON to this path instead of stdout
  --pretty              indent the JSON output (2 spaces) instead of compact
```

**"Compact" vs. "pretty" — the exact serialization calls, not left implicit:**
- Default (no `--pretty`): `json.dumps(rows, separators=(",", ":"), ensure_ascii=False)`
  — no spaces after `,`/`:` at all, and non-ASCII characters emitted as literal UTF-8
  rather than `\uXXXX`-escaped (§3 decision 11). (Plain `json.dumps(rows)` with no
  arguments is *not* this — it still inserts a space after each separator and escapes
  non-ASCII by default, both verified — so the call must pass both arguments explicitly.)
- `--pretty`: `json.dumps(rows, indent=2, ensure_ascii=False)`.

Exit codes: `0` success · `1` any handled error (see §4.5) with a one-line message on
stderr, no traceback (except the quiet `BrokenPipeError` case, §3 decision 16, which
exits 1 with no message) · `2` argparse's own usage/parse errors — a missing required
positional, an unrecognized flag, `--pretty=foo`, `-o` with no value, an invalid
subcommand, or the missing-subcommand case (§4.5, §3 decision 15) — argparse's default
behavior, not a custom message, and never a raw traceback for any of the three codes.

### 4.5 Failure modes (concrete, not "handle errors")

Per §3 decision 10, filesystem-level failures (the first six rows below) are **all**
handled by one `except OSError as e:` clause in `cli.py`, formatted as
`csv2json: <path>: {e.strerror}` (input side) or `csv2json: cannot write <path>: {e.strerror}`
(`-o` side) — the specific message varies naturally with `e.strerror`, without the design
needing to enumerate each `OSError` subclass. The rows below are the instances this spec
specifically verified live, **not an exhaustive list** — that's the point of decision 10.

| Failure | Behavior |
|---|---|
| Input path doesn't exist | stderr: `csv2json: <path>: No such file or directory` · exit 1 |
| Input path is a directory | stderr: `csv2json: <path>: Is a directory` · exit 1 |
| Input file exists but isn't readable (permission denied) | stderr: `csv2json: <path>: Permission denied` · exit 1 |
| `-o` path's parent dir doesn't exist | stderr: `csv2json: cannot write <path>: No such file or directory` · exit 1 |
| `-o` path is itself an existing directory | stderr: `csv2json: cannot write <path>: Is a directory` · exit 1 |
| A path component of `-o` is a file, not a directory (e.g. `-o existing_file.txt/out.json`) | stderr: `csv2json: cannot write <path>: Not a directory` · exit 1 |
| Input file isn't valid UTF-8 | stderr: `csv2json: <path>: not valid UTF-8` · exit 1 *(`UnicodeDecodeError` — a separate `except` clause, not the `OSError` catch; see §4.1)* |
| Empty file (no header at all) | stderr: `csv2json: <path>: empty input: no header row` · exit 1 |
| Blank first line (header reads as 0 columns) | stderr: `csv2json: <path>: empty input: no header row` · exit 1 (same message as the row above — both are "no real header", see §3 #7) |
| Duplicate header column | stderr: `csv2json: <path>: duplicate header column: '<name>'` · exit 1 |
| Header-only file (0 data rows) | stdout: `[]` (or written to `-o`) · exit 0 — **not** an error |
| Ragged data row | stderr: `csv2json: <path>: row N: expected W fields, got G` · exit 1 |
| A blank line in the data region (not the header) | skipped silently — **not** an error, no object appended (§3 #12) |
| A field exceeds the stdlib `csv` module's field-size limit (131072 bytes by default) | stderr: `csv2json: <path>: <the csv.Error message>` · exit 1 |
| `python3 -m csvkit` invoked with no subcommand | prints usage to stderr · exit 2 (argparse's own default for a missing required subcommand — not a custom message) |
| Output piped into a consumer that closes early (`\| head`, `\| less -p`, …) — `BrokenPipeError` | **no stderr message** · exit 1 — quiet, not an error (§3 decision 16) |
| A non-pipe stdout write failure (rare — e.g. redirected to a full disk) | stderr: `csv2json: error writing output: <e.strerror>` · exit 1 (no path token — stdout has none) |

---

## 5. Phasing & ordering

Single phase — the feature is small enough that splitting it would be ceremony, not
value (tight scope / YAGNI).

**File-touch / concurrency map:**

| File | Touched by | Concurrency |
|---|---|---|
| `csvkit/convert.py` | Task 1 | new file — no conflict |
| `csvkit/cli.py` | Task 2 | new file — no conflict |
| `csvkit/__main__.py` | Task 2 | new file — no conflict |
| `tests/test_convert.py` | Task 1 | new file — no conflict |
| `tests/test_cli.py` | Task 2 | new file — no conflict |

All five are new files with no shared hub — genuinely disjoint, though this project is
small enough (and single-writer) that sequential execution is still the right call. (The
formal execution-approach decision, per Ritual 8, belongs in PLAN.md once it's written —
not cited here in advance of that document existing.)

---

## 6. Backward compatibility & risk

- **Compatibility:** N/A — this is the first feature in a greenfield project; no
  existing callers, tests, or contracts to break.
- **Risks:**
  - *Risk:* `csv.reader`'s handling of unusual encodings (non-UTF-8 files) is
    unspecified in this design. *Mitigation:* open the file in text mode with
    `encoding="utf-8-sig"` explicitly (§3 decision 9) and let a `UnicodeDecodeError`
    surface as a clean stderr message (same handled-error pattern as the other failure
    modes) rather than silently mis-decoding — named explicitly as a task-level
    acceptance check.
  - *Risk:* a leading UTF-8 BOM (common in Excel's "CSV UTF-8" export) silently
    corrupts the first header name, and CRLF line terminators inside a quoted field are
    silently rewritten by Python's text-mode newline translation — both verified live in
    §2 on a real file, both invisible to any test using `io.StringIO`. *Mitigation:*
    `encoding="utf-8-sig", newline=""` on every `open()` call (§3 decision 9); §7 adds
    live-verification rows using real fixture files on disk, not in-memory strings.
  - *Risk:* very large CSV files are fully loaded into memory (`csv_to_json_rows`
    returns a list, not a generator). *Mitigation:* accepted for v1 — streaming is
    unscoped complexity for a first feature (YAGNI); if a real large-file case shows up,
    it's a natural, isolated v2 change to `convert.py`'s return type. Not backlogged
    speculatively — no concrete case exists yet.
- **Rollback:** the whole feature is additive (new files only); reverting is `git revert`
  the feature commit(s), no migration needed.

---

## 7. Verification strategy

**Pure-logic claims (`convert.py`) — automated behavioral unit tests:**

| Claim to verify | How |
|---|---|
| A well-formed CSV converts to the correct JSON-ready list of dicts | Feed a small in-memory CSV, assert the exact resulting list of dicts. |
| Quoted fields with embedded commas and embedded newlines round-trip correctly | Test using the exact fixture probed live in §2. |
| An escaped (doubled) quote round-trips to a single literal quote | Test using the exact fixture probed live in §2 (`"he said ""hi"""` → `he said "hi"`). |
| A short ragged row raises `RaggedRowError` with the correct 1-indexed data-row number | Test with a short row; assert the exception and its `.row_number`. |
| A long ragged row raises `RaggedRowError` with the correct 1-indexed data-row number | Test with a long row; assert the exception and its `.row_number`. |
| A ragged row is reported by **data-row count**, not physical file line, when an earlier row contains an embedded newline | Test combining §2's embedded-newline fixture with a following ragged row (locks in §3 decision 2's chosen behavior — the exact combination this round's review caught as untested). |
| A header-only file (valid header, zero data rows) returns `[]` | Behavioral unit test. |
| A genuinely empty file (`""`) raises `EmptyInputError` | Behavioral unit test. |
| A file whose first line is blank also raises `EmptyInputError` (not a confusing width-0 ragged-row error) | Behavioral unit test — locks in §3 decision 7. |
| A duplicate header column raises `DuplicateHeaderError` naming the offending column | Behavioral unit test. |
| A blank line in the data region is skipped — no dict appended — and a *following* ragged row still reports the correct data-row number (the blank row still consumes an `enumerate` index) | Behavioral unit test combining a blank data row with a following ragged row (§3 decision 12). |

**CLI-surface claims (`cli.py`) — live verification** (Ritual 6: a CLI a human runs and
reads output from is a real user-facing surface, not exempt "pure backend" — every claim
below is driven for real against a real file on disk, not asserted from a function call):

| Claim to verify | How |
|---|---|
| Converting a real file on disk prints correct JSON to stdout | Run `python3 -m csvkit csv2json <fixture>`, capture and inspect real stdout. |
| `-o <path>` writes the JSON to that file instead of stdout | Run with `-o`, read the real file back, inspect its content. |
| `--pretty` produces indented (2-space) output; its absence produces truly separator-compact output (no spaces — see §4.4) | Run both ways, inspect the real captured bytes for each. |
| A missing input file exits 1 with the exact documented stderr message, no traceback | Run against a nonexistent path, inspect real stderr text + exit code. |
| A directory given as input exits 1 with the exact documented stderr message | Run against a real directory path, inspect real stderr text + exit code. |
| An empty input file exits 1 with the exact documented stderr message | Run against a real empty fixture file, inspect real stderr text + exit code. |
| A ragged-row input exits 1 with the exact documented stderr message (including the `csv2json: <path>:` prefix that only `cli.py` adds, not `convert.py`) | Run against a real ragged fixture file, inspect real stderr text + exit code. |
| A duplicate-header input exits 1 with the exact documented stderr message | Run against a real duplicate-header fixture file, inspect real stderr text + exit code. |
| `-o` to a path whose parent directory doesn't exist exits 1 with the documented stderr message | Run with `-o /nonexistent-dir/out.json`, inspect real stderr text + exit code. |
| `-o` to a path that is itself an existing directory exits 1 with the documented stderr message | Run with `-o` pointed at a real directory, inspect real stderr text + exit code. |
| A non-UTF-8 input file exits 1 with the exact documented stderr message | Run against a real fixture file containing invalid UTF-8 bytes, inspect real stderr text + exit code. |
| A CRLF-terminated real file with an embedded-newline quoted field round-trips with the `\r\n` byte-exact (not silently rewritten to `\n`) | Write a real fixture file to disk (not `io.StringIO` — this bug is invisible to in-memory strings, see §2), run the CLI, inspect the real captured JSON output bytes. |
| A real file with a leading UTF-8 BOM has it stripped from the first header's JSON key (not left as a literal `﻿` prefix) | Write a real BOM-prefixed fixture file to disk, run the CLI, inspect the real captured JSON output. |
| A real blank-first-line fixture exits 1 with the **same** stderr message/prefix as the genuinely-empty-file case (not just correct at the pure-logic level) | Run against a real blank-first-line fixture file, inspect real stderr text + exit code — confirms the `csv2json: <path>:` CLI prefix is applied on this path too. |
| A real header-only fixture, run through the CLI, prints exactly `[]` to stdout and exits 0 | Run against a real header-only fixture file, inspect real stdout + exit code — the CLI-level counterpart to the pure-logic test above (a success case, not just the failure paths). |
| An unreadable (permission-denied) input file exits 1 with the exact documented stderr message | Run against a real `chmod 000` fixture file, inspect real stderr text + exit code. |
| A path component of `-o` being a file (not a directory) exits 1 with the exact documented stderr message | Run with `-o` pointed through a real file as if it were a directory (e.g. `-o realfile.txt/out.json`), inspect real stderr text + exit code. |
| `-o` pointed at the **same path as the input** file, when the input doesn't exist, reports the **input**-side error (not the `-o`-side one) | Run `csv2json missing.csv -o missing.csv`, confirm the stderr message uses the `csv2json: <path>: …` prefix, not `cannot write` — the case §3 decision 13 specifically hardens. |
| A CSV cell containing non-ASCII text (e.g. an accented name) round-trips as literal UTF-8 in the JSON output, not `\uXXXX`-escaped | Run against a real fixture with non-ASCII content, inspect the real captured output bytes for literal UTF-8 (§3 decision 11). |
| A real fixture with a blank line in the data region converts correctly through the CLI — the blank line produces no JSON object | Run against a real fixture file with a blank line between data rows, inspect the real captured JSON output (§3 decision 12). |
| Output piped into a truncating consumer (`\| head -c N`) produces no stderr message and a clean exit — not a raw `BrokenPipeError` traceback or "Exception ignored" spam | Run `python3 -m csvkit csv2json <large-fixture> \| head -c 5`, inspect real captured stderr (must be empty) and the exit code of the left side of the pipe (§3 decision 16). |
| A non-pipe stdout write failure (rare — e.g. a full disk) exits 1 with the path-less error message — **not** the `-o`-side message, and not a raw traceback | A real full-disk condition isn't practically reproducible as a fixture file; **monkeypatch `sys.stdout.write`** to raise a non-`BrokenPipeError` `OSError` (e.g. `OSError(28, "No space left on device")`) while driving `cli.main()`, assert the exact stderr text `csv2json: error writing output: No space left on device` and exit code 1 — this deliberately departs from this table's usual "drive a real file on disk" method, since this one failure mode can't be produced that way (§3 decision 16). |
| A field exceeding the stdlib's field-size limit exits 1 with a clean message, not a raw `csv.Error` traceback | Run against a real fixture with an oversized quoted field, inspect real stderr text + exit code (§3 decision 14). |
| `python3 -m csvkit` with no subcommand exits 2 with usage on stderr, not a raw `AttributeError` traceback | Run with zero arguments, inspect real stderr text + exit code (§3 decision 15). |
| `-h`/`--help` prints the exact contract shown in §4.4 | Run `python3 -m csvkit csv2json -h`, diff the real output against §4.4's captured block. |

---

## 8. Open decisions (for the owner)

None — all decisions settled in §3. This is a solo, low-stakes side project; nothing
here rises to a genuine gray-area fork that needs to be reserved rather than made by the
author and recorded.

---

## 9. Self-review log (the author owns the gate)

Run via 2 fresh-context reviewer subagents per round (distinct lens emphasis, same
frozen snapshot), collapsed conservatively (round is CLEAN only if every reviewer is
clean) — per `core/03-REVIEW-GATES.md` §6's "breadth within a round" pattern.

| Round | Lens emphasis | Findings | Result |
|---|---|---|---|
| 1 (foundational) | broad quality sweep (re-derived §2 probes live) + coherence/verification-strategy scrutiny | 1 blocker + 6 major + 5 minor, both lenses independently found overlapping real defects: incomplete/undefined exception contract (blocker); "line" vs. "row" numbering contradiction; a genuine silent-data-loss bug in duplicate headers (not previously considered); two citations (`docs/PROJECT_RULES.md`, `docs/BACKLOG.md`) pointing at content that didn't exist; under-covered §7 verification table; an unprobed blank-first-line edge case. All spot-verified independently before fixing (see conversation). | **fail** — fixed: added `EmptyInputError`/`DuplicateHeaderError` definitions + full exception enumeration in §4.1/§4.2; renamed "line" → "data-row" throughout with rationale (§3 #2); added duplicate-header detection (§3 #8, §4.3) and blank-first-line handling (§3 #7, §4.3); added a real locked decision to `docs/PROJECT_RULES.md` and 5 real rows to `docs/BACKLOG.md`; expanded §7 to cover every §4.5 failure mode individually; captured the real argparse `-h` output instead of hand-typing it; defined "compact" precisely (`separators=(",", ":")`). |
| 2 | backward-compat/cross-artifact consistency + no-placeholders/docs-currency (fresh reviewers, given round 1's findings ledger, told to report only NEW issues) | 3 major + 3 minor. Two majors were self-inflicted regressions from round 1's own fix pass (§3 decision 1 still said `DictReader` after §4.3 had been changed to bare `csv.reader`; §7's expansion missed a UTF-8-validity row). The third major was genuinely new and the sharpest finding of the whole cadence: opening the file without `newline=""` silently rewrites an embedded `\r\n` inside a quoted field to `\n` on any CRLF-terminated file — invisible to every `io.StringIO`-based probe/test in the spec, only reproducible against a real file on disk. A linked minor (UTF-8 BOM corrupting the first header) came from the same "test with a real file, not a string" instinct. All three majors independently re-verified live before fixing. | **fail** — fixed: reworded §3 decision 1 to name `csv.reader` (not `DictReader`) with the rationale for why; added §3 decision 9 (`encoding="utf-8-sig", newline=""`) with both gotchas probed live on real files in §2; updated §4.1's file-open description and §6's risk list; added a `-o`-is-a-directory failure mode to §4.5; added 4 new §7 live-verification rows (UTF-8 validity, CRLF preservation, BOM stripping, `-o`-is-a-directory), on top of the embedded-newline+ragged-row combination row already added in round 1; softened §5's premature PLAN.md citation. |
| 3 | drift vs. live reality (rebuilt convert.py + a faithful cli.py from the spec and re-tested) + completeness/currency (1:1 §7-vs-§4.5 audit, §9 arithmetic check) | 1 blocker + 1 major + 3 minor. The blocker: the exception catalog was STILL incomplete after two rounds of fixing it — a reviewer who actually implemented cli.py from the spec's contract found `PermissionError` and `NotADirectoryError` both leak raw tracebacks, and the one generic "OSError" item already listed was a mislabeled duplicate of the already-caught `FileNotFoundError` case, not real coverage of the gap. Also: §7's CLI table still had 2 failure modes (blank-first-line, header-only) verified only at the pure-logic level, never through the CLI wrapper; a stale "only" in §2's file-state description; a real arithmetic error in round 2's own log entry; and json.dumps's default `ensure_ascii=True` silently escaping non-ASCII CSV content, never decided either way. All spot-verified live before fixing. | **fail** — fixed: replaced the itemized OSError enumeration with one blanket `except OSError as e:` (§3 decision 10) formatted via `e.strerror` — eliminates the whole class of "missed a subclass" bugs that had now recurred twice; verified `e.strerror` text for all 4 concrete instances (`FileNotFoundError`, `IsADirectoryError`, `PermissionError`, `NotADirectoryError`) before writing them into §4.5; added the 2 missing §7 CLI-surface rows; decided `ensure_ascii=False` explicitly (§3 decision 11) and reflected it in §4.4's exact serialization calls; fixed the §2 wording and the §9 round-2 arithmetic. |
| 4 | implement-and-attack (actually wrote convert.py + cli.py from the spec text alone into a scratch dir, then attacked the running code with real files) + full top-to-bottom document audit | 2 blockers + 3 majors. Blocker 1: a blank line in the *data* region (not just the header, which round 1 already handled) was misclassified as a ragged row — verified live that an ordinary trailing-blank-line file (a very common real-world shape) would be incorrectly rejected. Blocker 2: `csv.Error` (e.g. the stdlib's field-size limit) is not a `ValueError`, `OSError`, or `UnicodeDecodeError` — none of the 5 existing except clauses caught it, so it leaked a raw traceback, the exact defect class that was blockers in rounds 1 and 3. Major: the single `OSError` clause's two message-prefix templates had no specified discriminator, and the obvious implementation (comparing `-o`'s path to the input path) breaks when the two paths happen to be equal. Major: `python3 -m csvkit` with no subcommand crashed with a raw `AttributeError` — `add_subparsers` needs `required=True`, which the spec never said. Major: §7 still had 4 settled §3/§4.5 claims (permission-denied-via-CLI, NotADirectory-via-CLI, non-ASCII round-trip, and the new blank-data-row/csv.Error/no-subcommand cases) with no verification row. All reproduced and confirmed live before fixing — this is now the *third* round to find a genuinely new gap in the exception-handling contract, which is itself a durable lesson (see the judgment writeup). | **fail** — fixed: added §3 decisions 12–15 (skip blank data rows; a phase-flag discriminator for the OSError message prefix, not path comparison; a 6th `except csv.Error` clause with an explicit YAGNI call on the field-size limit; `required=True` on the top-level subparser); updated §4.1 to six except clauses + the phase flag + the subparser fix; updated §4.3's code to skip blank data rows with a comment cross-referencing decision 7's header-only precedent; added 3 new §4.5 rows and **5** new §7 rows covering permission-denied-via-CLI, NotADirectory-via-CLI, non-ASCII round-trip, csv.Error-via-CLI, and no-subcommand-via-CLI. *(Correction, caught by round 5: this entry originally claimed 6 new §7 rows — it was actually 5; the blank-data-row case itself was missed and had zero §7 coverage until round 5 added it.)* |
| 5 | attack-from-a-different-angle (piping, arg combinations, TOCTOU-adjacent, multi-duplicate headers) + full-document consistency (recounted the except-clause claim precisely, re-audited §7-vs-§4.5 1:1, re-checked §9's own log accuracy) | 3 major. The sharpest: round 4's own `reading_done` phase-flag fix only modeled TWO write destinations (`-o` or not), but there are genuinely THREE outcomes (reading, writing to `-o`, writing to stdout) — a stdout write failure (most commonly `BrokenPipeError` from piping into `\| head`, an entirely ordinary usage pattern) fell into the `-o`-side branch and produced the broken message `csv2json: cannot write None: Broken pipe`, verified live. A second major: §7 still had zero coverage for round 4's own blank-data-row fix (see round 4's corrected log entry above) — the exact bug class that was a round-4 blocker had no regression test named anywhere. A third finding overlapped the second (same root cause, different phrasing). This is the *fourth* round to find a genuinely new gap in the exception/output-handling contract — see the judgment writeup for what that recurrence means. | **fail** — fixed: added §3 decision 16 (a dedicated `BrokenPipeError` clause — quiet exit, not an error message, per Python's own documented SIGPIPE idiom — plus a path-less message for the rare non-pipe stdout failure); updated §4.1 to **seven distinct exception types** (loosened from a literal clause-count claim per a round-5 minor) in the correct more-specific-first order; added 2 new §4.5 rows; added 3 new §7 rows (blank-data-row pure-logic test, blank-data-row-via-CLI, broken-pipe-via-CLI) — closing both round 5's new finding and round 4's own coverage gap in the same pass; folded in both round-5 minors (a single-column blank-row caveat on decision 12; the except-clause-count wording). Independently re-verified the whole design with a 3rd from-scratch implementation before spending round 6. |
| 6 | implement-a-4th-time (fresh scratch build, no peeking at prior implementations; multi-line CRLF/LF, symlinks, malformed-flag argparse errors, the full 0/1/2 exit-code contract, deep duplicate-header cases, unicode beyond BOM) + reviewable-artifact quality (citation-number audit across the whole doc, §9 log fidelity spot-check) | 2 major (both lenses independently converged on the **same** gap) + 1 minor. Significant signal: **the 4th independent implementation found zero new runtime defects** — every §4.5/§7 scenario, plus new ones (mocked non-pipe stdout failure, multi-duplicate headers, real broken-pipe-via-`head`), matched the documented behavior exactly. What both lenses found instead was a pure documentation-completeness gap: round 5's own new §4.5 row ("non-pipe stdout write failure") never got a matching §7 verification row — round 5's log claimed a "1:1 audit" but missed the row it had just added two lines above. The minor: §4.4's exit-code summary never mentioned exit code 2 (argparse's own usage-error code), even though §4.5 and §3 decision 15 both already documented a case that uses it. | **fail** (on the floor of correctness — a coverage gap, not a functional bug) — fixed: added the missing §7 row (naming the monkeypatch technique needed, since a full-disk condition can't be reproduced as a real fixture file); extended §4.4's exit-code sentence to cover all three codes (0/1/2) explicitly. |
| 7 | final-implement-check (an independent from-scratch implementation, ~25 real-file scenarios) + final-document-audit (doc-model compliance, "ready for PLAN.md?") | **The spec's *content* is clean** — the implement-check lens (yet another independent build — reviewers across rounds 3-7 have each rebuilt convert.py/cli.py from the spec text; the exact count was never rigorously tracked, but it is several, not a marginal one or two) found zero new runtime defects across every §4.5/§7 scenario plus new ones (multi-line CRLF/LF, symlinks, malformed argparse flags, the full 0/1/2 exit-code contract, deep duplicate-header cases, unicode beyond BOM), including a byte-for-byte match of the real `-h` output. But the document-audit lens found 1 major + 2 minor **outside SPEC.md itself**: `docs/NEXT-STEPS.md` §1 and `docs/README.md`'s "Start here" block both still said "pre-work, about to brainstorm" — stale by 6 full review rounds, sending a cold reader backward to redo finished work (exactly the front-door-currency lens the completion ritual itself checks for, and exactly what Ritual 10 exists to catch — this is a genuine self-inflicted drift, not a nitpick: the review cycle's own intensity meant the front door never got reconciled along the way). Two minors: SPEC.md/BACKLOG.md/PROJECT_RULES.md were still uncommitted after 6 rounds of edits (violates CLAUDE.md's "commit docs at every milestone boundary"); and this table's own "fail" streak means the formal 2-consecutive-clean exit condition is not literally met yet by round count, even though the underlying content risk is now very low. | **fail** — fixed: reconciled `NEXT-STEPS.md` §1 and `docs/README.md`'s cursor to reflect "SPEC done, PLAN next" (both mirrors, same pass, per Guardrail A); will commit the spec + its doc-model fixes as the "spec complete" checkpoint. On the streak-honesty point: **explicit judgment call, recorded here rather than left implicit** — content risk is now genuinely low (several independent implementations across rounds 3-7, 0 outstanding functional defects), but the cadence's own rule is followed literally rather than judgment-called away: round 8 will run as a true attempt at the second consecutive clean round before the spec is called converged. |
| 8 | implement-once-more (yet another independent from-scratch build) + doc-funnel-and-git-state currency | 1 major + 2 minor. Content lens: **clean** — no new runtime defect. Doc-funnel lens: found the **same defect class as round 7, in a third file** — the repo-**root** `README.md` (distinct from `docs/README.md`) still said "Just bootstrapped. No commands exist yet," never touched by round 7's reconcile or the spec-convergence commit. This is exactly why Ritual 10's sweep needs an explicit, named surface list rather than relying on "the front-door docs" as a vague category — round 7 fixed the two files that came to mind first and missed the third. Minors: the self-review log's own "Nth independent implementation" labels had drifted internally inconsistent (3rd → 4th → 6th, skipping a 5th) — a cosmetic accuracy gap, not a substantive one. | **fail** — fixed: reconciled the root `README.md`'s Status section to match the other two front-door files; **promoted this as a carry-forward checklist** in `docs/PROJECT_RULES.md` naming all three front-door surfaces explicitly (root `README.md`, `docs/README.md`, `docs/NEXT-STEPS.md` §1), so a future reconcile has a checklist instead of relying on memory (Ritual 12); softened the implementation-count language throughout to avoid asserting precision that was never actually tracked. |
