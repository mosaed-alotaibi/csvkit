# Project rules — csvkit

<!-- A THIN per-project rules file. It does NOT restate the Keelwright rituals — it -->
<!-- ADOPTS them by reference, then adds only what is specific to THIS project. -->
<!-- Keeping the rituals in one canonical place (the installed Keelwright core) means -->
<!-- they evolve once and every project inherits the change. -->

> Long-lived rules that apply across every milestone, plan, and session.
> They supersede defaults in any tool's heuristic where they conflict — the
> owner is in control.

---

## The standing rituals (adopted from Keelwright)

This project adopts the Keelwright lifecycle and review gates **by reference**. Do not
copy them here — read them at their canonical location so updates flow through:

| Layer | Where it lives | What it covers |
|---|---|---|
| Tool-agnostic methodology | [`core/02-RITUALS.md`](/Users/mosae/projects/keel/core/02-RITUALS.md) | The lifecycle loop, the review gates, the pre-done confirmation ritual, verification doctrine, the per-session capture rituals |
| Tool mapping (this project's agent) | [the adapter for your agent](/Users/mosae/projects/keel/adapters/claude-code) | How the rituals map onto this project's concrete tooling (independent-reviewer mechanics, durable cross-session notes, hooks) |

<!-- keel init GUESSED ../../keelwright/core (assumes a sibling dir literally named -->
<!-- "keelwright"). Repointed to the real local checkout below, which is named "keel" -->
<!-- (the framework was renamed Keel→Keelwright but this local clone dir wasn't; see -->
<!-- the locked-decision note under Project-specific conventions). Absolute path used -->
<!-- since csvkit and keel are unrelated sibling dirs, not nested. -->

**The rituals at a glance** (full text lives in `core/02-RITUALS.md`):

1. Completion ritual — before any "done": multiple independent re-audit rounds, exit only on consecutive clean passes.
2. Verification-driven, not test-mechanical — tests derive from claims and verify behavior at real surfaces.
3. Proactive-but-cautious tool use — proactive on safe operations; confirm before destructive ones.
4. Don't hand-curate tool-owned state — leave tool-owned state directories/files to their tool.
5. Coherence audit after each design/spec/plan artifact, before it reaches the owner.
6. Live verification for any UI / behavioral surface before claiming it works.
7. Test-effectiveness audit — passing ≠ effective.
8. The author owns the review gate — iterative self-review to convergence; the owner delegates and spot-checks.
9. Context budget & proactive handoff — keep the resume cursor always current.
10. State-change currency — reconcile front-door docs + notes after any state change.
11. (Conditional) External-dependency feedback — capture friction with off-limits / third-party components.
12. Lessons-learned capture — one dated file per session.
13. Parallel-agent synchronization — read-only fan-out free; writers only on disjoint files; rituals single-writer.
14. Documentation model & anti-drift — the BACKLOG→ROADMAP→NEXT-STEPS→PRD funnel; stable IDs; one canonical location per item.
15. Housekeeping adjudication — agent-originated destructive cleanup gets one bounded adversarial pass before acting; owner-requested chores are exempt.
16. Dependency-reality check — verify an unfamiliar / fast-moving / post-cutoff dependency against the installed package's source/types before designing on it; pin the version.

<!-- Trim or extend this list to the rituals your project actually adopts. -->
<!-- If you adopt all of Keelwright core, leave it as-is; if you drop some, say so here. -->

---

## Project-specific conventions

<!-- This is the ONLY part that is genuinely per-project. Put here the things -->
<!-- Keelwright core cannot know: naming/brand rules, hub files that must serialize, -->
<!-- environment specifics, locked owner decisions, stack-bound conventions. -->
<!-- Each entry should be a durable rule, not a transient note. -->

<!-- Example shapes (delete and replace):

### Naming / brand
- Visible brand = {{BRAND_VISIBLE}}; technical identifiers = csvkit.
- Locked owner decisions go here so the codebase never silently contradicts them.

### Hub files (serialize writers — see Ritual 13)
- {{HUB_FILE}} is the convergence point; one writer at a time; no worktrees over it.

### Environment / stack conventions
- Python 3 (stdlib only)-specific commands, layouts, or invariants that every session must honor.

### Locked decisions
- 2026-07-01 — mosalotaibi: {{DECISION}} (rationale, scope).
-->

### Locked decisions

- **2026-07-01 — mosalotaibi:** Keelwright core/adapter paths above are pinned to the
  absolute local path `/Users/mosae/projects/keel` (not a relative `../../keelwright/`
  guess) because the local checkout directory is still named `keel`, not `keelwright`.
  If that directory is ever renamed, update this file and the paths above together.
- **2026-07-01 — mosalotaibi:** `.keelwright/` (the marker, memory seeds, hook snippet)
  is **committed**, not gitignored. Reasoning: nothing in it is tool-regenerated —
  it's one-time install output meant for a human to read or copy elsewhere — so
  Ritual 4 ("don't hand-curate tool-owned state") doesn't apply to it.

---

## Where these rules live

- **This file** (`docs/PROJECT_RULES.md`) — the per-project layer: the adoption
  pointer above + the project-specific conventions. Durable in the repo, survives
  context resets, applies to all future milestones.
- **Keelwright core** (`core/02-RITUALS.md`) — the canonical, tool-agnostic ritual text.
  Update the rituals there; this file only references them.
- **The tool adapter** (`adapters/<your-agent>/`) — maps the rituals onto the
  concrete agent/tooling, including any durable cross-session notes the agent keeps.

Update this file and the canonical ritual text together when a rule evolves.
