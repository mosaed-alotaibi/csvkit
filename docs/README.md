# Project Docs — csvkit

<!-- The docs front door. The FIRST file anyone (human or AI agent) opens. -->
<!-- Keep it thin: it routes, it does not duplicate. Every fact lives in exactly -->
<!-- one canonical doc (see the source-of-truth map); this file only points. -->

**Open this first** — the docs front door + source-of-truth map.

---

## Start here (fresh context)

<!-- One short, ALWAYS-CURRENT pointer to where work resumes. A reader with zero -->
<!-- prior context must land on the CURRENT milestone, never a shipped one. -->
<!-- Reconcile this block after every state change (push/merge/seal/branch). -->
<!-- Prefer a single live cursor over a pile of dated history blocks. -->

> **▶ CURRENT (2026-07-01):** v1 (csv2json) is ready for integration on
> `codex/csv2json`; the full suite, live CLI checks, and completion review are green.
> Fresh-reviewer independence was unavailable and is recorded as a seal caveat.
> **Authoritative current cursor = [NEXT-STEPS.md](NEXT-STEPS.md) §1.**

<!-- Optional: collapse older "where we were" notes into ROADMAP.md history, not here. -->
<!-- If you must keep dated history blocks, label them clearly as history. -->

The standing engineering rules are in [`PROJECT_RULES.md`](PROJECT_RULES.md).

---

## The source-of-truth map

<!-- The ONE canonical map — one doc per concern. No other doc duplicates it. -->
<!-- Add/remove rows to match the docs this project actually keeps. -->

This is the **one** canonical map — one doc per concern. No other doc duplicates it.

| Concern | Canonical doc |
|---|---|
| Repo onboarding / how to run | [`../README.md`](../README.md) |
| Docs index + this map | `README.md` |
| How to resume / what's next | [`NEXT-STEPS.md`](NEXT-STEPS.md) |
| The plan (milestones + history) | [`ROADMAP.md`](ROADMAP.md) |
| Ideas / deferrals (parking lot) | [`BACKLOG.md`](BACKLOG.md) |
| What the system is (as-built reqs) | [`PRD.md`](PRD.md) |
| QA scope (what's testable today) | [`AS-BUILT-FOR-QA.md`](AS-BUILT-FOR-QA.md) |
| Component wiring & swap guide | [`STACK_WIRING.md`](STACK_WIRING.md) |
| Standing engineering rules | [`PROJECT_RULES.md`](PROJECT_RULES.md) |
| Designs / specs | [`spec-and-plan/`](spec-and-plan/) <!-- specs + plans share this dir; split into spec-and-plan/specs and /plans if you prefer --> |
| Implementation plans | [`spec-and-plan/`](spec-and-plan/) <!-- same dir as the row above; split out /plans if you prefer separate trees --> |
| Per-session lessons learned | [`lessons-learned/`](lessons-learned/) |
| Verification evidence | [`verification/`](verification/) |
| Keelwright dogfood assessment | [`KEELWRIGHT-ASSESSMENT.md`](KEELWRIGHT-ASSESSMENT.md) |
| Operational how-tos | [`guides/`](guides/) |
| History / superseded docs | Future `archive/` directory (none needed yet) |
<!-- | External-dependency feedback (Ritual 11) | [`EXTERNAL-DEP-FEEDBACK.md`](EXTERNAL-DEP-FEEDBACK.md) | (only if you keep an off-limits-component feedback log) -->
<!-- | {{CONCERN}} | [`{{DOC}}`]({{DOC}}) | -->

---

## How the docs connect

<!-- A small ASCII map so a reader sees the funnel at a glance. -->
<!-- Mirror the rows above; keep the funnel direction obvious. -->

```
docs/README.md ─ you are here (front door + source-of-truth map)
   │
   ├─▶ BACKLOG.md ──── ideas / deferrals (parking lot)
   ├─▶ NEXT-STEPS.md ── §1 = authoritative current cursor (always up to date)
   ├─▶ ROADMAP.md ───── the plan (milestones + history)
   ├─▶ PRD.md ───────── what the system is (as-built requirements)
   ├─▶ AS-BUILT-FOR-QA.md  what's actually testable today
   ├─▶ STACK_WIRING.md  component wiring + how to swap each piece
   ├─▶ PROJECT_RULES.md  the standing engineering rules
   ├─▶ spec-and-plan/ ─ design specs + implementation plans
   ├─▶ lessons-learned/  per-session issues + mitigations + lessons
   ├─▶ verification/ ──── dated review evidence + findings ledgers
   │
   └─▶ archive/ ─────── future history / superseded docs (not created yet)
```

The docs form a funnel: **BACKLOG → ROADMAP → NEXT-STEPS → PRD** (ideas/deferrals →
the plan → how-to-resume → as-built). Each fact lives in exactly one canonical doc;
every other mention references it by ID and never restates the detail.

<!-- Module-specific docs live WITH their module (e.g. a service's own README), -->
<!-- not here. Link to them rather than copying their content. -->

---

## Archive

No historical document has been superseded yet, so `archive/` does not exist. Create it
with an index when the first real artifact is archived; do not reference it before then.
