# csvkit — Agent Operating Guide

<!-- This is the project CLAUDE.md. Claude Code reads it at session start.
     Fill the {{PLACEHOLDERS}}, delete these comments, commit it to the repo root. -->

Owner: mosalotaibi
Stack: Python 3 (stdlib only)
Repo: /Users/mosae/projects/csvkit

This project follows the **Keelwright** methodology. Authority and details live in the docs funnel — this file is the pointer, not the spec.

## Read these first

| Doc | Purpose |
|---|---|
| `docs/README.md` | Docs index + source-of-truth map — the **front door**. |
| `docs/PROJECT_RULES.md` | The rituals + working agreements. **Authoritative.** Honor every rule. |
| `docs/BACKLOG.md` | Raw ideas, stable IDs. |
| `docs/ROADMAP.md` | Sequenced milestones. |
| `docs/NEXT-STEPS.md` | The live resume cursor + safe-resume prompt. **Start here each session.** |
| `docs/PRD.md` | What the system is today (as-built requirements). |

The funnel direction is `BACKLOG → ROADMAP → NEXT-STEPS → PRD`. One canonical home per item; reference others by ID.

## Defaults (non-negotiable)

- **Evidence over claims.** Never assert "it works", "tests pass", or "done" without a captured artifact — command output, a screenshot, a query result. No eval-gaming. If you didn't run it, say so.
- **Proactive but cautious.** Reads, inspects, builds, and tests need no permission — just run them, but understand the effect first. Surface destructive or irreversible operations for confirmation before running.
- **Tight scope.** Do the asked-for thing; flag adjacent work, don't silently expand. Recommend, don't unilaterally decide.
- **Harden by default.** A working *and* hardened result beats a fast one. Close latent risks while the context is fresh. When in doubt, harden.
- **Don't hand-curate tool-owned state.** A planning/automation tool regenerates its own state directory — gitignore it, never hand-edit it. The durable trail is the docs funnel + commit history; commit docs at every milestone boundary.

## Honor the rituals

The rituals in `docs/PROJECT_RULES.md` are mapped to concrete Claude Code mechanics in
Keelwright's `adapters/claude-code/rules/RITUALS-IN-CLAUDE-CODE.md`. In particular:

<!-- That file lives in your Keelwright install (wherever you cloned or vendored Keelwright),
     not inside this project — open it from your Keelwright copy. -->


- **Before any "done" or `/clear`:** run the completion ritual — fresh audit subagents, ≥2 consecutive clean rounds.
- **For any spec/plan/design you produce:** own the review gate (min 3 iterations, exit on 2 consecutive clean) and run one coherence pass.
- **For any UI/behavioral surface:** verify live before claiming it works (headless-browser driver in `scripts/`).
- **After any state change (push/merge/seal/branch):** reconcile the front-door docs + durable notes so the cursor is never stale.
- **At session end:** append lessons-learned; keep the handoff current so `/clear` is always safe.

## Choosing your execution shape

Name the shape before you start; don't default to inline.

- Gated chain → sequential subagents.
- Decomposable fan-out (judge panel, adversarial verify, loop-until-converged) → the Workflow tool.
- Reusable named procedure → a Skill.
- Trivial → inline.

> To run a *gate* (review rounds) or *execute* as a parallel swarm **without** weakening the
> cadence, follow Keelwright's `adapters/claude-code/rules/GATED-SWARM.md` — fan out the work, keep
> the streak/verdict/funnel single-owned.

## Durable notes

Cross-session facts live in auto-memory, indexed by `MEMORY.md`. One fact per file; keep the index hooks short. When something durable changes, update the relevant memory and the `NEXT-STEPS.md` cursor in the same breath.
