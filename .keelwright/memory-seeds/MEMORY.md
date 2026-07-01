# Memory Index

<!--
Claude Code auto-memory lives outside the repo, per-project, and persists across sessions.
This file is the INDEX. Keep it to one line per memory:
    - [Title](file.md) — short hook (why you'd open it)
Order by importance, not alphabetically. The index is what the agent skims first.
-->

## How memory works

| Type | Prefix | Holds |
|---|---|---|
| user | `user_` | Facts about the owner/team (timezone, contact, hard preferences). |
| feedback | `feedback_` | Durable working agreements + rituals the owner has reinforced. |
| project | `project_` | Project-specific state, decisions, history pointers. |
| reference | `reference_` | Reusable how-tos, locations, doctrine the agent looks up. |

Rules:
- **One fact per file.** A memory file is a single durable idea, not a journal.
- **Frontmatter schema** on every file:
  ```
  ---
  name: <short-kebab-case-slug>
  description: <one-line hook — what this memory is for>
  metadata:
    node_type: memory
    type: user | feedback | project | reference
  ---
  ```
  `name` is a short kebab-case slug (e.g. `review-gate`), not a prose title.
  `node_type: memory` is the field the Claude Code auto-memory harness tags each
  node with — include it so hand-authored files match what Claude Code writes
  itself. (Claude Code also adds bookkeeping fields like `originSessionId`
  automatically; you don't author those.)
- **Link between memories** with `[[slug]]` — the target memory's `name:` slug
  (kebab-case), not its filename. The harness resolves the link by the slug.
- Update the relevant memory the moment a durable fact changes — same breath as the `docs/NEXT-STEPS.md` cursor.
- When a memory goes stale, fix it in place; leave project *history* alone (rephrase, don't rewrite the past as if it never happened).

## Index

<!-- Seed entries below. Replace/extend with your project's memories. See _SEED_MEMORIES.md. -->

- [Evidence over claims](feedback_evidence_over_claims.md) — never assert without a captured artifact; no eval-gaming.
- [Completion ritual before "done"/clear](feedback_completion_ritual.md) — ≥2 consecutive clean fresh-context audit rounds.
- [Assistant owns the review gate](feedback_review_gate.md) — self-review spec/plan, min 3 iters, exit on 2 clean.
- [Proactive but cautious](feedback_proactive_but_cautious.md) — run reads/builds/tests freely; surface destructive ops.
- [State-change currency](feedback_state_change_currency.md) — after push/merge/seal, reconcile front-door docs + memory.
- [Context budget & handoff](feedback_context_handoff.md) — no self-meter; keep the handoff always-current so clear is safe.
- [Doc funnel](reference_doc_funnel.md) — BACKLOG→ROADMAP→NEXT-STEPS→PRD; stable IDs, one canonical home.
- [Tool-owned state is not yours to hand-curate](feedback_tool_owned_state.md) — gitignore the planning tool's state dir; the trail is your docs + commit history; commit docs at every milestone.

<!-- - [{{TITLE}}]({{TYPE}}_{{slug}}.md) — {{hook}} -->
