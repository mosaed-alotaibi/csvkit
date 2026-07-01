# {{FEATURE_NAME}} — Implementation Plan

<!-- The IMPLEMENTATION PLAN: the spec turned into ordered, verifiable tasks. -->
<!-- One canonical SPEC is its source of truth (link it below). The plan itself -->
<!-- passes the author's review gate (iterative self-review to convergence) before -->
<!-- execution. Tasks use checkbox syntax so any executor (a fresh agent session, a -->
<!-- second AI, or a person) can work through them and a reviewer can track progress. -->
<!-- This is verification-driven, NOT mechanical: each task names what to verify and -->
<!-- how, at a real surface. -->

> **For executors:** work this plan **task by task**. Each task ends with a
> **verification** step and a commit. Do not mark a task done until its
> verification passes with shown evidence (Keelwright verification doctrine).

**Goal:** {{ONE_LINE_GOAL}}

**Architecture:** {{HOW_THE_PIECES_FIT}} <!-- the shape of the change in 2–4 sentences -->

**Stack:** Python 3 (stdlib only) <!-- the concrete tech/versions this plan assumes -->

**Spec (source of truth):** [`{{SPEC_PATH}}`]({{SPEC_PATH}})

**Branch:** `{{BRANCH}}` (off `{{BASE_BRANCH}}`)

---

## Invariants (hold across every task)

<!-- The hard constraints that span ALL tasks — true before the first task and -->
<!-- still true after the last. Every executor reads these once and honors them -->
<!-- throughout: off-limits paths, the green-test floor, no-touch surfaces, and the -->
<!-- merge/stop boundary. If a task would violate an invariant, STOP and surface it. -->

- **Off-limits — never edit:** {{INVARIANT}} <!-- e.g. vendored/3rd-party paths, generated artifacts -->
- **Green-test floor:** {{INVARIANT}} <!-- e.g. the existing N tests stay green with zero edits -->
- **No-touch surfaces:** {{INVARIANT}} <!-- e.g. a byte-faithful proxy / public contract left untouched -->
- **Merge boundary:** the owner owns all merges — when the work is built and gated, **state ready and stop** (do not merge).
<!-- Add project-specific invariants. If a constraint applies to only one task, it -->
<!-- belongs in that task, not here. -->

---

## Material findings vs. the spec (read before executing)

<!-- Facts discovered while planning that the spec under-states and that change the -->
<!-- plan's shape. If reading the code revealed something, record it here so the -->
<!-- executor isn't surprised. If none, say "None — spec verified accurate." -->

1. {{FINDING_THAT_CHANGES_THE_PLAN}}
2. {{FINDING}}

---

## File-touch map (serialize the hub — Ritual 13)

<!-- Which files each task touches, and the concurrency it implies. Multiply-touched -->
<!-- files (above all the hub) serialize; disjoint streams may run in parallel. -->

| File | Touched by | Concurrency |
|---|---|---|
| {{HUB_FILE}} | {{TASKS}} | **SERIAL** — one task at a time |
| {{DISJOINT_FILE}} | {{TASKS}} | **PARALLEL-SAFE** — disjoint |

**Single working tree; commit per task.** {{ANY_GATE_COMMANDS_TO_RUN_BETWEEN_TASKS}}

---

## Boot & verification commands (verbatim — do NOT invent flags)

<!-- The exact, copy-pasteable commands an executor uses to boot the stack and -->
<!-- verify. Pin real flags/ports. Include the live-verification command for UI/ -->
<!-- behavioral surfaces (Ritual 6) and the test/typecheck commands. -->

```bash
# Boot the stack:
{{BOOT_COMMANDS}}

# Run the test suite / typecheck:
{{TEST_COMMANDS}}

# Live-verify a UI / behavioral surface (capture evidence):
{{LIVE_VERIFY_COMMANDS}}
```

---

## Tasks

<!-- Each task: a clear deliverable, the files it touches, the concrete steps, and -->
<!-- an explicit VERIFICATION with expected output. Keep tasks small enough to commit -->
<!-- atomically. Number them; phase them if the spec is phased. -->

### Phase 1 — {{PHASE_NAME}}

#### Task 1 — {{TASK_TITLE}}

- **Files:** {{FILES}}
- **Steps:**
  - [ ] {{STEP}}
  - [ ] {{STEP}}
- **Verify:** {{WHAT_TO_CHECK}} → expected: {{EXPECTED_OUTPUT_OR_SCREENSHOT}}.
- **Commit:** `{{COMMIT_MESSAGE_SHAPE}}`

#### Task 2 — {{TASK_TITLE}}

- **Files:** {{FILES}}
- **Steps:**
  - [ ] {{STEP}}
- **Verify:** {{WHAT_TO_CHECK}} → expected: {{EXPECTED}}.
- **Commit:** `{{COMMIT_MESSAGE_SHAPE}}`

### Phase 2 — {{PHASE_NAME}}

#### Task 3 — {{TASK_TITLE}}

- **Files:** {{FILES}}
- **Steps:**
  - [ ] {{STEP}}
- **Verify:** {{WHAT_TO_CHECK}} → expected: {{EXPECTED}}.
- **Commit:** `{{COMMIT_MESSAGE_SHAPE}}`

<!-- Add tasks until the spec is fully covered. Every spec requirement must map to -->
<!-- at least one task (cross-artifact consistency — coherence audit lens). -->

---

## Phase gates

<!-- A checklist run at the end of each phase before moving on: the test suite -->
<!-- green, typecheck clean, live verification captured, docs/notes reconciled. -->

- [ ] All Phase tasks committed.
- [ ] Test suite green: {{TEST_COMMAND}} → {{EXPECTED}}.
- [ ] UI/behavioral surfaces live-verified with evidence (Ritual 6).
- [ ] Front-door docs + resume cursor reconciled (Ritual 10).

---

## Execution-approach decision

<!-- Per Keelwright Ritual 8, the executor DECIDES (not asks) how to orchestrate -->
<!-- execution and records it: does the work decompose into independent units -->
<!-- (parallel fan-out) or is it a gated chain / trivial task (sequential / inline)? -->
<!-- Weigh fit + context cost; explicitly consider whether parallel fan-out beats a -->
<!-- sequential approach for this plan, and name why the chosen approach won. -->

**Chosen approach:** {{APPROACH}} <!-- e.g. sequential single-writer (hub serializes); parallel fan-out on the disjoint doc stream -->
**Why:** {{RATIONALE}} <!-- fit + context-window cost; why this beats the alternative -->

---

## Self-review log (the author owns the gate)

<!-- The iterative self-review of THIS plan (min iterations, exit on consecutive -->
<!-- clean passes), distinct from the spec's. Record findings per iteration. -->

| Iteration | Lens emphasis | Findings | Result |
|---|---|---|---|
| 1 (foundational) | {{LENS}} | {{FINDINGS}} | {{fix/clean}} |
| 2 | {{LENS}} | {{FINDINGS}} | {{fix/clean}} |
| 3 | {{LENS}} | {{FINDINGS}} | {{clean}} |

**Outcome:** {{CONVERGED_OR_CONTINUE}} — {{NEXT_STEP}}.
