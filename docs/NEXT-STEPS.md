# Next steps — how to resume safely and what's next

<!--
  THE most important doc in Keelwright. It is the durable runbook for resuming after a
  context reset (a new session, a different agent, a different person). It answers
  exactly two questions:
    1. Where are we RIGHT NOW? (the cursor — §1)
    2. How do I continue WITHOUT breaking what's done? (baseline + guardrails + resume prompt)

  Funnel position: BACKLOG → ROADMAP → NEXT-STEPS → PRD.
  NEXT-STEPS §1 is the SINGLE SOURCE OF RESUME TRUTH. ROADMAP points here for "where
  we are"; this doc must always be current. After any state change (push / merge /
  ship / defer / branch), reconcile §1 in the same pass — drift here is dangerous
  because it's what a cold session trusts.

  Keep history lines as-is once written; add new state, mark old cursors HISTORICAL.
-->

> Durable runbook for resuming after a context reset. Authoritative for "what's next
> + how to start without breaking what we've done." Pairs with
> [`PROJECT_RULES.md`](PROJECT_RULES.md) (standing rules). The live contract is the
> code itself + [`PRD.md`](PRD.md); older handoffs are archived under `archive/`.
> **Last updated:** 2026-07-01 — <!-- one line: most recent state; the §1 cursor is authoritative -->

---

## 1. Where we are (the current cursor — do NOT break this)

<!-- ============================================================================
     THIS BLOCK IS THE SINGLE SOURCE OF RESUME TRUTH.
     A fresh session should be able to read ONLY this section and know:
       - what is DONE and proven (with evidence pointers)
       - what is IN FLIGHT and on which branch
       - what the very next action is, and who owns it
     Keep it tight. Push detail into specs/plans/archive and link out.
     ============================================================================ -->

> **▶ CURRENT INITIATIVE (2026-07-01) — v1 (csv2json).**
> GOAL: ship a v1 CLI that converts a CSV file to JSON.
> STATE: SPECCED — `docs/spec-and-plan/SPEC.md` is complete and implementation-ready.
>
> **Audited maturity / readiness:** scaffold ~100% · spec content ~100% (several
> independent from-scratch implementations across rounds 3–10 found and fixed every
> runtime defect surfaced, most recently a `sys.stdout.flush()` gap in the
> `BrokenPipeError` handling — round 10 — that silently only worked for large output)
> · plan/execution ~0%.
> Current gates: green baseline (1/1 test passing); the review cadence itself has
> **not yet** hit its 2-consecutive-clean exit — rounds 1–6 found real content defects;
> round 7 found content clean but 2 front-door files stale (fixed); round 8 found content
> clean but a 3rd front-door file stale (fixed); **round 9 was the first fully clean
> round (streak 1/2)**; round 10 reset the streak — a genuine content blocker (the
> flush() gap) plus this cursor itself going stale *again* (the exact recurring pattern
> the carry-forward checklist exists to prevent — see the lessons-learned entry). Both
> fixed. See `docs/spec-and-plan/SPEC.md` §9 for the full round-by-round log.
> **Next: two consecutive genuinely clean rounds are needed to converge the cadence
> formally — round 11 restarts the attempt.** No plan written yet.
>
> **Workstreams / open gaps (evidence-backed):**
> - **A · implementation plan** — SPEC.md is done; PLAN.md is still the raw template
>   scaffold (`{{FEATURE_NAME}}` etc.) and needs to be written next.
>
> **Locked architecture / decisions (do not relitigate):** Python 3, stdlib only, no
> third-party dependencies (see `docs/PROJECT_RULES.md`); the full csv2json design in
> `docs/spec-and-plan/SPEC.md` §3 (16 settled decisions) — don't relitigate without a
> new real case per the tight-scope/YAGNI principle.

**▶ NEXT ACTION (who owns it):** Write `docs/spec-and-plan/PLAN.md` from the settled SPEC.md, then run its own review cadence — owner: whoever picks up this project next.

<!-- Below the live cursor, keep a short DONE record of recently-completed milestones,
     newest first, each one line with its proof + branch. Mark superseded cursors
     HISTORICAL rather than deleting them — a cold reader needs to trust that the old
     lines were true when written. -->

> **✅ DONE — SPEC.md content** *(branch `main`, 2026-07-01)*: zero outstanding runtime defects across several independent from-scratch implementations (rounds 3–10, most recently the round-10 `sys.stdout.flush()` fix); the review *cadence* itself is still converging (streak reset at round 10) — see `docs/spec-and-plan/SPEC.md` §9.
> **✅ DONE — Bootstrap** *(branch `main`, committed 2026-07-01)*: `keel init` run, doc funnel installed, package scaffold + test harness in place, baseline green (`python3 -m unittest discover -s tests -v` → 1/1 passing).
> **⚠ HISTORICAL** — "Pre-work — about to brainstorm v1 scope" (true on 2026-07-01 at bootstrap; superseded by the live cursor above once SPEC.md was written and reviewed).

**▶ RESUME PROMPT — paste in a clean session to continue this initiative:**

<!-- A self-contained block a fresh session can paste verbatim. It must NOT rely on
     conversation memory. Include: the goal, today's state, "design-first vs execute",
     the FIRST files to read in order, the workstreams, the locked decisions, the
     people/constraints, and the literal first step. See §6 for the full template. -->

```
RESUME — csvkit: v1 bootstrap.
Repo: /Users/mosae/projects/csvkit. Follow PROJECT_RULES.md; durable notes auto-load (see the adapter for your agent).

GOAL: ship a v1 CLI that converts a CSV file to JSON.
TODAY: the doc funnel is installed and a green baseline (1/1 test) is committed on
main. No feature code exists yet.

DESIGN-FIRST: brainstorm → spec → plan → execute.

FIRST READ (in order): NEXT-STEPS.md §1 (this cursor) → docs/PROJECT_RULES.md → docs/BACKLOG.md → csvkit/__init__.py.

WORKSTREAMS: A · brainstorm + spec the v1 (csv2json) scope.
LOCKED DECISIONS: Python 3, stdlib only, no third-party dependencies.
PEOPLE/CONSTRAINTS: solo project, no external reviewers.

FIRST STEP: brainstorm the v1 scope, then write docs/spec-and-plan/SPEC.md.
```

## 2. Milestone history (condensed)

<!-- Optional. A condensed trail of past milestones for a reader who wants context
     beyond the current cursor. One short paragraph or a few lines per milestone,
     with pointers to the archived detail. Don't let this grow unbounded — archive. -->

None yet — this is the first milestone.

## 3. The proven loop (how every change is made)

<!-- One line: the lifecycle every change follows. Reference PROJECT_RULES.md for the
     full ritual rather than restating it. -->

`brainstorm` (get owner approval) → **spec** → **plan** → execute (fresh implementer +
independent review per task) → **verify live** → **re-run the full gate matrix** →
**seal ritual** (two consecutive clean re-audit rounds) → commit per task → push.
The reviewer owns the spec/plan/execution review gate. See [`PROJECT_RULES.md`](PROJECT_RULES.md).

## 4. Establish the GREEN BASELINE before touching anything (the safety net)

<!-- The exact commands to reach a KNOWN-GOOD line BEFORE making any change. This is
     the single most valuable thing a resuming session can do: prove the system is
     green first, so any later difference is YOUR change, not a pre-existing mystery.
     Fill in the real boot/test/verify commands and the expected outputs. -->

```
No external dependencies to start — stdlib only, no datastore, no env files.
python3 -m unittest discover -s tests -v     # expect: Ran 1 test ... OK  <- known-good line
```

There is no long-running server or UI to boot yet — v1 is a CLI invoked per-run.
**If the test command above is green, it's your known-good line** — any later
difference is your change, not a mystery.

> **Resting mode (2026-07-01):** no config profiles yet — single dev mode. Tests always
> run against the stdlib-only toolchain (no network, no external services).

## 5. Guardrails (non-negotiable)

<!-- The hard rules a resuming session must not violate. Include the ones specific to
     THIS project (off-limits dirs, branch convention, things that must stay green,
     known-flaky-not-regression facts, push/merge gating). Be blunt. -->

- **Branch convention** — trunk-based on `main`; no protected branches yet (single-dev project).
- **No off-limits areas yet** — the whole tree is fair game; this section will grow as real constraints emerge.
- **Additive + tested.** Don't regress the passing test suite (currently 1/1 — grows with each task).
- **No known flaky tests or ceiling facts yet.**
- **Push/merge only what the owner approves.** Stop and confirm at every milestone (the seal ritual).
- **No network access in tests.** csvkit is stdlib-only and offline by design — a test that reaches the network is a bug, not a feature.

## 6. Paste-ready resume prompt (full template)

<!-- A fuller, reusable resume-prompt scaffold for any future initiative. The §1 block
     is the LIVE one; this is the shape to fill when a new initiative begins. Keep
     superseded prompts below, marked HISTORICAL, for the trail. -->

```
RESUME — csvkit: {{INITIATIVE}} ({{ONE_LINE_STATE: e.g. "design-first" / "execute plan at task N" / "built, awaiting MR"}})
Repo: /Users/mosae/projects/csvkit. Follow PROJECT_RULES.md; durable notes auto-load.

CONTEXT: {{2-4 SENTENCES — what is done + proven, what is in flight + on which branch, what the next action is}}.

FIRST READ (in order): NEXT-STEPS.md §1 (the authoritative cursor) → {{SPEC}} → {{PLAN}} → {{ENTRYPOINT}}.

LOCKED DECISIONS (mosalotaibi, 2026-07-01): {{NON-NEGOTIABLE_FACTS}}.

HOW IT'S BEING BUILT: {{THE_LOOP — fresh implementer per task, independent review between, live verify, seal ritual}}.

BRANCH: {{BRANCH}} ({{ALREADY_CUT / TO_CUT_OFF_X}}) — {{DO_NOT_RE-CUT / next is the MR}}.

OWNER/DEVOPS HANDOFF (if any): {{THE_HUMAN-GATED_ACTIONS_AND_WHO_OWNS_THEM}}.

GUARDRAILS: {{OFF-LIMITS}}; {{TEST_FLOOR}}; {{LIVE-VERIFY_REQUIREMENT}}; {{PUSH/MERGE_GATING}}.
```

> **⚠ HISTORICAL resume prompts** — kept below for the trail; superseded by the §1 cursor.

<!-- Paste superseded prompt blocks here, each preceded by a HISTORICAL note + its date. -->
