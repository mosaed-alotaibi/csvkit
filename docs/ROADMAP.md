# Roadmap — csvkit

<!--
  The plan + the history. ROADMAP owns the ORDER of work and the honest record of
  what shipped, what was removed, and what was reprioritized. It does NOT restate
  item detail — that lives in BACKLOG.md by ID (one canonical location per item).

  Funnel position: BACKLOG → ROADMAP → NEXT-STEPS → PRD.
  ROADMAP sits in the middle: it pulls prioritized items from BACKLOG and feeds the
  current cursor to NEXT-STEPS. The authoritative "where we are right now" cursor is
  NEXT-STEPS §1 — this doc points there, it does not duplicate it.

  Anti-drift: when a milestone state changes (built / shipped / deferred / reverted),
  reconcile this doc in the same pass. Leave history lines as-is; add new state, don't
  rewrite the past.
-->

> New here? Open the [docs index](README.md) first, then the resume runbook
> [`NEXT-STEPS.md`](NEXT-STEPS.md).
> **Last updated:** 2026-07-01 — <!-- one line: the most recent state change + current focus -->
> **Authoritative current cursor = [`NEXT-STEPS.md` §1](NEXT-STEPS.md).**
> **Plan owner:** mosalotaibi.

This is the **current plan**.
<!-- If you keep a detailed early/legacy phase map, archive it (don't inline it here)
     and link the archive directory below. Delete the line if you have no archive. -->
Older/detailed phase maps are archived under [`archive/`](archive/).

## 1. What shipped (Delivered)

<!-- The done work, newest-relevant first or in phase order. Each row: what + the
     honest state (with the proof — test count, gate passed, live-verified). Link to
     archived handoff notes rather than inlining detail. -->

As-built detail: [`PRD.md`](PRD.md).

| Phase / Milestone | What | State |
|---|---|---|
| {{PHASE_OR_MS}} | {{WHAT_WAS_BUILT}} | ✅ {{PROOF}} |
| {{PHASE_OR_MS}} | {{WHAT_WAS_BUILT}} | ✅ {{PROOF}} |
| {{PHASE_OR_MS}} | {{WHAT_WAS_BUILT}} | ✅ {{PROOF}} |

## 2. Planned milestones (the real plan)

<!-- The forward plan, ordered. Each milestone: a status tag in parentheses
     (planned / in-progress / BUILT-not-merged / DONE), the goal in one or two
     sentences, and pointers to its spec/plan if they exist. Reference removed items
     by BL-id; record the milestone's removed/deferred items in §2.1, not inline. -->

- **{{MILESTONE_NAME}}** *(status: {{PLANNED | IN-PROGRESS | BUILT-NOT-MERGED | DONE}}; on branch `{{BRANCH}}`)*.
  {{GOAL_IN_ONE_OR_TWO_SENTENCES}}. Spec [`{{SPEC_PATH}}`]({{SPEC_PATH}}) · plan [`{{PLAN_PATH}}`]({{PLAN_PATH}}).
  - **Removed (recorded in [`BACKLOG.md`](BACKLOG.md) by BL-id — see §2.1):** {{SUMMARY}} ({{BL-IDS}}).
  - **Kept / clarified:** {{WHAT_STAYED_AND_WHY}}.
  - **Added:** {{NEW_CAPABILITY}}.
- **{{NEXT_MILESTONE_NAME}}** *(status: {{...}})*. {{GOAL}}.

### 2.1 Removed / Deferred record — {{MILESTONE_NAME}}

<!-- Honest record of what a milestone removed. Detail lives ONCE in BACKLOG.md by
     BL-id (this references by ID, it does not restate). Distinguish "parked
     (backlogged)" from "intentionally removed, NOT backlogged". -->

| What was removed | Destination |
|---|---|
| {{REMOVED_ITEM}} | → **{{BL-ID}}** (parked) |
| {{REMOVED_ITEM}} | **NOT backlogged — intentional** ({{WHY_NO_REVIVAL_PATH}}) |

**Kept (not removed):** {{WHAT_STAYED}}.

## 3. Reprioritized backlog (re-framed)

<!-- When a pivot changes the priority of previously-planned work, record the new
     status here by reference. Don't restate the item — name it and give its new
     standing (absorbed / lower-priority / blocked / deployment-driven). -->

| Item | New status |
|---|---|
| {{ITEM}} | **{{ABSORBED_BY / LOWER-PRIORITY / BLOCKED / DEPLOYMENT-DRIVEN}}** — {{WHY}} |
| {{ITEM}} | {{...}} |

## 4. How we work

<!-- Point at the Keelwright rituals/rules; do not duplicate them here. -->

Every change goes through the proven loop and the standing rules — see
[`PROJECT_RULES.md`](PROJECT_RULES.md) (the Keelwright lifecycle loop, review gate, and
seal ritual). Resume via [`NEXT-STEPS.md`](NEXT-STEPS.md).
