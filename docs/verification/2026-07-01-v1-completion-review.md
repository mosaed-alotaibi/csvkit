# v1 completion review — 2026-07-01

**Scope:** the whole `codex/csv2json` change: implementation, tests, CLI surface,
as-built docs, front doors, commit narrative, and repository state.

**Cadence:** Keelwright heavy gate — minimum 3 serialized rounds; stop only after two
consecutive clean rounds. A clean round means no new open blocker/major finding; minors
must be dispositioned. The first round is groundwork and never counts toward exit.

**Independence caveat:** the implementation seal was run by the same executor because
fresh review agents were unavailable in this run. The cadence, distinct lenses, live
checks, and mutation tests were preserved, but strict fresh-context independence was
not. This is qualified convergence, not a claim that the unavailable condition was met.

## Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| CR-001 | major | Explicit `-o ""` was tested by truthiness and silently fell back to stdout instead of treating the supplied value as an output path. | **fixed** — regression test first (observed exit 0), then `args.output is not None`; test and full suite green. |
| CR-002 | minor | Generated live placeholders remained in BACKLOG and guides, including a broken guide link. | **fixed** — removed live template residue; retained only commented authoring examples. |
| CR-003 | minor | `CLAUDE.md` told a CLI project to use a nonexistent browser driver. | **fixed** — replaced with the real CLI verification surface and exact observable outputs. |
| CR-004 | minor | The lessons entry described 9 review rounds after the spec actually converged at 12. | **fixed** — reconciled the dated entry to the completed cadence. |
| CR-005 | minor | Living docs referenced an `archive/` index/directory that does not exist yet. | **fixed** — describe it as a future resource and provision it only when first needed. |

## Round log

| Round | Primary lenses and concrete checks | Result |
|---|---|---|
| 1 — groundwork | Broad requirements/code/test/doc sweep. Read production code and tests; traced SPEC §7 to behavior; searched living docs for stale state, placeholders, and broken references. Reproduced CR-001 by proving argparse returns `''` (`False` by truthiness but not `None`), then observed the new regression test fail with exit 0. | **FAIL** — CR-001 major plus CR-002–005 minors; all fixed. Clean streak 0. |
| 2 | Coherence, backward compatibility, and test effectiveness. Full suite with `ResourceWarning` escalation; compileall; stdlib-import/dependency check; live Markdown-link resolution; main-to-branch diff check. Mutation audit removed `sys.stdout.flush()` (test caught exit 120), removed `newline=""` (test caught CRLF corruption), and bypassed duplicate-header validation (test caught silent overwrite); each mutation was restored before the full run. | **CLEAN** — no new open finding. Streak 1. |
| 3 | Cold-user and handoff completeness. Ran README commands against real multilingual/embedded-newline CSV; inspected compact stdout and pretty output file; checked missing-input, duplicate-header, explicit-empty-output, and closed-pipe stderr/exit behavior; reviewed all three front doors and both repositories' state. | **CLEAN** — no new open finding. Streak 2; floor met. |
| 4 | Durability and factual accuracy of the newly written evidence ledger, implementation lesson, and Keelwright assessment. Rechecked every numeric and historical claim against tests, commits, and the dogfood trail; resolved all live relative links; reran the full suite. | **CLEAN** — no new open finding. Post-record streak 1. |
| 5 | Final artifact integrity, scope containment, and cold-resume accuracy. Verified production/tests were unchanged after Round 3, the new docs stay inside csvkit, front doors still pointed at the correct pending action, and the Keelwright checkout remained clean; reran compileall and all 39 tests. | **CLEAN** — no new open finding. Post-record streak 2. |

The core change converged after Round 3. Rounds 4–5 then confirmed the durability and
accuracy of this record, the lessons entry, and the Keelwright assessment added after
core convergence.

## Evidence captured

- `python3 -W error::ResourceWarning -m unittest discover -s tests -v` — 39 tests,
  0 failures.
- `python3 -m compileall -q csvkit tests` — exit 0.
- Live compact stdout preserved literal Arabic and embedded-newline data.
- Live `--pretty -o` produced an indented UTF-8 JSON file and empty stdout.
- Missing input: exit 1, exact one-line `No such file or directory` message.
- Duplicate header: exit 1, exact one-line duplicate-column message.
- Explicit empty output path: exit 1, output-side message; no silent stdout fallback.
- Immediately closed pipe: exit 1, zero stderr bytes.
- All live relative Markdown links resolve.
- Production imports are Python stdlib or local package imports; no dependency manifest.
- `/Users/mosae/projects/keel` remained clean; no Keelwright source file was changed.

## Outcome

**QUALIFIED CONVERGENCE.** Five rounds ran; Round 1 failed and was fixed, Rounds 2–5
were clean, and the final two post-record rounds were consecutive clean passes. The
implementation and handoff meet the tested v1 contract. Strict Keelwright
fresh-context independence was not available, so that condition remains an explicit
caveat rather than a hidden claim. Integration remains an owner decision.
