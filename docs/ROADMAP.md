# Roadmap — csvkit

> New here? Open the [docs index](README.md), then the authoritative resume cursor in
> [`NEXT-STEPS.md` §1](NEXT-STEPS.md).
> **Last updated:** 2026-07-01 — v1 reviewed and ready for integration.
> **Plan owner:** mosalotaibi.

ROADMAP owns milestone order and history. Detailed design belongs in the spec, live
resume state belongs in NEXT-STEPS, and deferred ideas live once in BACKLOG.

## Milestones

| Milestone | What | State and proof |
|---|---|---|
| Bootstrap | Keelwright doc funnel, package scaffold, and test harness | ✅ DONE — `keel init`; baseline committed |
| v1 design | `csv2json` behavior and execution plan | ✅ DONE — [SPEC](spec-and-plan/SPEC.md) converged after 12 rounds; [PLAN](spec-and-plan/PLAN.md) converged after 6 |
| v1 build | Stdlib-only CSV-to-JSON conversion and CLI | **READY FOR INTEGRATION — QUALIFIED SEAL** on `codex/csv2json`; full suite + live CLI + five-round completion review green, with fresh-reviewer caveat recorded |

## Current milestone — v1 integration decision

The completion review found and fixed one real CLI defect, then converged. The owner now
chooses merge, keep branch, or discard. See the dated
[`completion review`](verification/2026-07-01-v1-completion-review.md) for evidence and
the explicit fresh-reviewer-independence caveat.

Spec: [`spec-and-plan/SPEC.md`](spec-and-plan/SPEC.md) · plan:
[`spec-and-plan/PLAN.md`](spec-and-plan/PLAN.md) · as-built contract:
[`PRD.md`](PRD.md).

## Deferred from v1

The canonical details remain in [`BACKLOG.md`](BACKLOG.md): BL-001 through BL-005.
They are parked, not silently discarded.

## How we work

Every change follows the standing rules in [`PROJECT_RULES.md`](PROJECT_RULES.md).
Resume from [`NEXT-STEPS.md`](NEXT-STEPS.md), never from this historical overview.
