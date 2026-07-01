# csv2json (v1) — Implementation Plan

> **For executors:** work this plan **task by task**. Each task ends with a
> **verification** step and a commit. Do not mark a task done until its
> verification passes with shown evidence (Keelwright verification doctrine).

**Goal:** ship `csvkit csv2json` — a stdlib-only CLI that converts a CSV file to a JSON
array of objects.

**Architecture:** `csvkit/convert.py` holds pure conversion logic + 3 exception classes,
taking a file-like object and returning `list[dict]` — no I/O, no CLI concerns, fully
unit-testable in-memory. `csvkit/cli.py` holds all I/O and argument parsing: opens the
file with the exact encoding/newline handling SPEC.md §3 decision 9 settled, calls
`convert.py`, serializes with the exact `json.dumps` calls §4.4 settled, and translates
every exception into the exact stderr message + exit code SPEC.md §4.5 documents.
`csvkit/__main__.py` is the `python3 -m csvkit` entry point.

**Stack:** Python 3 (stdlib only) — `csv`, `json`, `argparse`, `os`, `sys`. No
dependencies to install.

**Spec (source of truth):** [`SPEC.md`](SPEC.md) — sealed, 12-round-converged (see its
§9). This plan does not restate design rationale; it sequences the settled design into
tasks. Every code shown here is SPEC.md's own §4 pseudocode, verified across 12 rounds —
this plan transcribes it, it does not re-derive it.

**Branch:** `codex/csv2json` (off `main`) in the isolated worktree
`.worktrees/csv2json`. The branch is still single-writer and sequential; isolation keeps
the sealed planning checkpoints on `main` untouched while implementation is in flight.

---

## Invariants (hold across every task)

- **Off-limits — never edit:** none — this is the first feature, nothing exists to
  protect yet.
- **Green-test floor:** the existing 1 test (`tests/test_package.py`) stays green with
  zero edits; every task only *adds* tests, never removes or weakens one.
- **No-touch surfaces:** none yet.
- **Merge boundary:** solo project, no external reviewer — the "owner" gate is the
  completion ritual (Task 2's phase gate + the project-level seal), not a human
  approval step.
- **Every exception message, exit code, and `json.dumps` call must match SPEC.md §4.4/
  §4.5 *exactly*** — those exact strings/codes were hardened across 12 review rounds
  (most notably the `sys.stdout.flush()` requirement in decision 16); deviating from
  them silently reopens a bug that took a dedicated round to close.

---

## Material findings vs. the spec

None — SPEC.md was verified against a real, running implementation many times over its
own 12-round review cadence (see its §9). Nothing here contradicts it; this plan is a
direct transcription into task order.

---

## File-touch map

| File | Touched by | Concurrency |
|---|---|---|
| `csvkit/convert.py` | Task 1 | new file — no conflict |
| `tests/test_convert.py` | Task 1 | new file — no conflict |
| `csvkit/cli.py` | Task 2 | new file — no conflict |
| `csvkit/__main__.py` | Task 2 | new file — no conflict |
| `tests/test_cli.py` | Task 2 | new file — no conflict |
| `docs/PRD.md`, `docs/AS-BUILT-FOR-QA.md`, `docs/STACK_WIRING.md` | Task 3 | new content in existing template files — serialize after Tasks 1–2 (as-built docs need the real build to describe) |

All five code files are new with no shared hub — genuinely disjoint — but this is a
single-writer solo project, so tasks run **sequentially** regardless (see the
execution-approach decision below).

**Single working tree; commit per task.** Between tasks: run
`python3 -m unittest discover -s tests -v` — must stay green.

---

## Boot & verification commands (verbatim)

```bash
# No boot step — csvkit is a CLI invoked per-run, not a long-lived server.

# Run the test suite:
python3 -m unittest discover -s tests -v

# Live-verify the CLI (Ritual 6 — a real user-facing surface, not "pure backend"):
python3 -m csvkit csv2json <real-fixture.csv>
```

---

## Tasks

### Phase 1 — Core conversion logic (`convert.py`)

#### Task 1 — `convert.py`: parsing, validation, and the three exception classes

- **Files:** `csvkit/convert.py` (new), `tests/test_convert.py` (new)
- **Steps:**
  - [x] Create `csvkit/convert.py` with `EmptyInputError`, `DuplicateHeaderError`,
        `RaggedRowError` (SPEC.md §4.2 — transcribe verbatim) and
        `csv_to_json_rows(fileobj) -> list[dict]` (SPEC.md §4.3 — transcribe verbatim,
        including the blank-header check, duplicate-header check, and the
        skip-blank-data-row-before-ragged-check ordering).
  - [x] Write behavioral unit tests for every row in SPEC.md §7's "Pure-logic claims"
        table (11 rows): well-formed CSV → correct dicts; embedded comma + newline;
        escaped (doubled) quote; short ragged row; long ragged row; ragged row reported
        by data-row count when an earlier row has an embedded newline (the combination
        test); header-only → `[]`; genuinely empty file → `EmptyInputError`; blank
        first line → `EmptyInputError`; duplicate header → `DuplicateHeaderError`;
        blank data row skipped + a following ragged row still gets the right data-row
        number.
- **Verify:** `python3 -m unittest discover -s tests -v` → all `test_convert.py` cases
  pass (expect 11+ tests: the 11 above, some may be split into 2 assertions each).
- **Commit:** `feat: convert.py — CSV parsing, validation, and exception classes`

### Phase 2 — CLI (`cli.py`, `__main__.py`)

#### Task 2 — `cli.py`: argument parsing, I/O, and exception-to-message translation

- **Files:** `csvkit/cli.py` (new), `csvkit/__main__.py` (new), `tests/test_cli.py` (new)
- **Steps:**
  - [x] Create `csvkit/cli.py` with `build_parser()` (SPEC.md §4.4's exact argparse
        contract: `input` positional, `-o/--output`, `--pretty`, subparser
        `required=True` per §3 decision 15) and `main(argv=None) -> int`.
  - [x] `main()` opens the input with `encoding="utf-8-sig", newline=""` (§3 decision 9),
        calls `convert.csv_to_json_rows`, sets `reading_done = True` on success (§3
        decision 13), serializes with the exact compact/pretty `json.dumps` calls (§4.4:
        `separators=(",", ":"), ensure_ascii=False` / `indent=2, ensure_ascii=False`),
        writes to `-o` or stdout.
  - [x] **The stdout write MUST be followed by `sys.stdout.flush()` inside the same
        `try`** (§3 decision 16 — this is the exact line that took a dedicated review
        round to catch; omitting it silently breaks the small-output broken-pipe case).
  - [x] Handle the 7 exception types/families in the required specificity order (§4.1):
        the 3 `convert.py`
        `ValueError`s + `csv.Error` (all formatted `csv2json: {input}: {e}`);
        `UnicodeDecodeError` (hardcoded "not valid UTF-8" message); `BrokenPipeError`
        (dedicated clause, before `OSError` — redirect stdout to `os.devnull`, exit 1,
        **no stderr message**); `OSError` (blanket, `e.strerror`-formatted, using
        `reading_done` + `args.output is not None` to pick one of the three message
        forms in §4.5).
  - [x] Create `csvkit/__main__.py` — `from csvkit.cli import main; import sys;
        sys.exit(main())`.
  - [x] Write CLI-surface tests for every row in SPEC.md §7's table without hardcoding
        a fragile row count. Drive the real command via `subprocess` against real fixture
        files on disk for every naturally reproducible behavior, inspecting real
        stdout/stderr/exit code. The one deliberate exception is the non-pipe stdout
        `OSError`: drive `cli.main()` while replacing `sys.stdout.write` with a writer
        that raises `OSError(28, "No space left on device")`, exactly as SPEC.md §7
        prescribes; a real full-disk condition is not a safe/reliable test fixture. This includes
        the **small**-fixture broken-pipe test (§3 decision 16's hardening — piping a
        small fixture into a reader that closes immediately, e.g. Python's own
        `subprocess.Popen` with a pipe closed after 1 read) *and* the large-fixture one;
        both must pass, not just the large one (the exact gap that survived rounds 5–9).
- **Verify:**
  1. `python3 -m unittest discover -s tests -v` → all tests pass (expect 30+ total
     across both test files).
  2. **Live-verify the CLI for real** (Ritual 6): create a real fixture CSV, run
     `python3 -m csvkit csv2json fixture.csv`, inspect the actual printed JSON. Run
     `python3 -m csvkit csv2json fixture.csv --pretty -o out.json` and `cat out.json`.
     Run `python3 -m csvkit csv2json nonexistent.csv` and confirm the exact documented
     stderr message + exit 1. Run `python3 -m csvkit csv2json fixture.csv | head -c 5`
     and confirm empty stderr + exit 1 (no traceback).
- **Commit:** `feat: cli.py — csv2json command, argument parsing, error handling`

### Phase 3 — As-built docs (only after the code is real)

#### Task 3 — Fill PRD.md / AS-BUILT-FOR-QA.md / STACK_WIRING.md from the real build

- **Files:** `docs/PRD.md`, `docs/AS-BUILT-FOR-QA.md`, `docs/STACK_WIRING.md`
- **Steps:**
  - [x] Fill PRD.md's FRs from the actually-built `csv2json` command (not from SPEC.md's
        intent — from what Tasks 1–2 actually produced; verify by reading the real code).
  - [x] Fill AS-BUILT-FOR-QA.md — csv2json is fully implemented, no mock/deferred
        surfaces to flag for v1.
  - [x] Fill STACK_WIRING.md — the convert.py/cli.py contract is the only "seam."
- **Verify:** every FR cites a real file/function that exists; `grep` confirms no
  `{{PLACEHOLDER}}` remains in the three files.
- **Commit:** `docs: fill PRD/AS-BUILT-FOR-QA/STACK_WIRING from the real v1 build`

---

## Phase gates

- [x] All 3 phases' tasks committed.
- [x] Test suite green: `python3 -m unittest discover -s tests -v` → all pass, 0
      failures.
- [x] CLI live-verified with evidence (Ritual 6) — real stdout/stderr/exit-code capture
      for the happy path and at least 3 failure modes, pasted into the session record.
- [x] Front-door docs + resume cursor reconciled (Ritual 10) — all three front-door
      surfaces (root `README.md`, `docs/README.md`, `docs/NEXT-STEPS.md` §1) updated in
      the same pass, per the carry-forward checklist in `docs/PROJECT_RULES.md`.

---

## Execution-approach decision

**Chosen approach:** Sequential, single working tree, inline (no subagent fan-out, no
Workflow tool).
**Why:** Per Ritual 8's fit + context-cost test — the three tasks are a **gated chain**
(Task 2 imports and calls Task 1's module; Task 3 describes what Tasks 1–2 built), not
independent units, so parallel fan-out would buy nothing. And the artifact is small
enough (3 production-code files, plus tests) that inline execution is
cheaper than the overhead of delegating to fresh subagent contexts. Fan-out is the right
call for decomposable, independent work or when the main context needs protecting from a
large search — neither applies here.

---

## Self-review log (the author owns the gate)

| Iteration | Lens emphasis | Findings | Result |
|---|---|---|---|
| 1 (foundational) | broad quality sweep — does every SPEC.md requirement map to a task? | Cross-checked: SPEC.md §4.1's 3 files (convert.py, cli.py, __main__.py) → Tasks 1–2; all 16 §3 decisions → traced into Task 1/2 steps; all ~32 §7 verification rows → traced into Task 1/2 verify steps. Found: the plan initially had no task for filling PRD.md/AS-BUILT-FOR-QA.md/STACK_WIRING.md from the real build — the doc-model's own PRD is "as-built," so it can't honestly be filled before code exists, but leaving it out entirely would mean sealing this milestone with 3 template files still full of `{{PLACEHOLDERS}}`. | fix — added Phase 3 / Task 3. |
| 2 | drift vs. SPEC.md — does every code snippet in this plan match SPEC.md's *current* (post-round-12) text exactly, not an earlier draft? | Re-read SPEC.md §4.2–§4.5 fresh and cross-checked every requirement named in Task 1/2 against the current file (the `sys.stdout.flush()` requirement, the 7-type/exception-order list, the `utf-8-sig`+`newline=""` open call, the exact `json.dumps` calls) — all consistent, no stale reference to an earlier (pre-round-10, pre-flush-fix) version of the design. | clean |
| 3 | well-specified + no-placeholders — is anything in this plan vague ("handle errors", "write tests") rather than concrete? | Re-read every step: each names an exact file, an exact behavior from SPEC.md, and an exact verification command. No step says "add tests" without naming which SPEC.md §7 rows the tests must cover. | clean |
| 4 (resume audit) | branch isolation + TDD executability + test-strategy fidelity | Found four real mismatches before implementation: the plan authorized direct work on `main`; Task 1 said §7 had 10 pure-logic rows but enumerated 11; Task 2 incorrectly required every CLI row to run through subprocess/real files even though SPEC.md explicitly requires a controlled `sys.stdout.write` failure for the non-pipe stdout `OSError`; and the execution rationale undercounted the production files. | **fail** — fixed: branch changed to isolated `codex/csv2json`; row count corrected to 11; subprocess-vs-controlled-failure strategy made explicit; production file count corrected. Front-door docs reconciled to PLANNED in the same pass. |
| 5 | requirement trace — all 16 decisions and every §7 row reachable from a task | Re-read SPEC.md §3 and §7 against Tasks 1–2. Decisions 1–8 and 12 map to Task 1 conversion tests/steps; decisions 9–11 and 13–16 map to Task 2 I/O/serialization/error tests/steps. Every pure-logic row is named in Task 1; Task 2 requires every CLI-surface row and explicitly preserves the one controlled-failure exception. | clean |
| 6 | cold-executor pass — can an executor implement without guessing? | Every task names files, exact API/flags, required ordering, red→green verification, live commands, and commit boundary. The sealed SPEC remains the canonical source for exact messages and pseudocode; no unresolved fork or live placeholder remains. | clean |

**Outcome:** Converged after the resume audit (floor exceeded; rounds 5–6 both clean) —
proceeding to isolated execution.
