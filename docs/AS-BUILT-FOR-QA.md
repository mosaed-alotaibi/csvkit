# csvkit — As-Built Scope for QA

**Derived from:** [`PRD.md`](PRD.md), audited against the code and live CLI on
2026-07-01.
**Audience:** QA and technical reviewers.

## 1. What the product is

csvkit v1 is a local, stdlib-only Python CLI. Its only product command is:

```sh
python3 -m csvkit csv2json INPUT [-o OUTPUT] [--pretty]
```

It reads one CSV file and emits a JSON array. There is no web UI, service, datastore,
network call, authentication layer, or background process.

## 2. Test environment

| Environment | What it covers | Prerequisites |
|---|---|---|
| Local checkout | Full functional and error-path scope | Python 3 only |

## 3. Testable — implemented behavior

| Area | Behavior | Verification surface |
|---|---|---|
| Parsing | ordinary rows; quoted commas/newlines; doubled quotes | `tests/test_convert.py` + real CLI |
| Validation | empty/blank header; duplicate header; short/long row; blank data line | unit + subprocess CLI tests |
| Output | compact stdout; `--pretty`; `-o/--output`; literal UTF-8 | subprocess CLI tests + live run |
| Encoding | UTF-8 BOM stripping; embedded CRLF preservation; invalid UTF-8 error | real on-disk fixtures |
| Filesystem errors | missing/directory/unreadable input; bad output paths | real on-disk fixtures |
| Process behavior | argparse exit 2; field-limit `csv.Error`; quiet broken pipe | subprocess tests |

## 4. Deferred — do not file as v1 bugs

`BL-001` JSON→CSV, `BL-002` type inference, `BL-003` custom delimiters, `BL-004`
headerless input, and `BL-005` installable packaging are intentionally parked in
[`BACKLOG.md`](BACKLOG.md).

## 5. Known limitations

- The full JSON array is held in memory; v1 is not a streaming converter.
- A bare blank line in a one-column CSV is skipped. To represent an explicit empty
  value, quote it as `""`.
- The stdlib CSV field-size limit remains unchanged; oversized fields fail cleanly.
- Input comes from a filesystem path, not stdin.

## 6. Canonical verification command

```sh
python3 -m unittest discover -s tests -v
```

Expected current evidence: **38 tests, 0 failures**.
