# Seed Memories — generalized bundle

Ready-to-use, project-agnostic memory files. Create each as its own `.md` file in your Claude Code auto-memory directory, then add its index line to `MEMORY.md` (see `MEMORY.md.tmpl`). One fact per file; frontmatter on every file.

These are the generalized equivalents of a mature project's `feedback_*` / `reference_*` memories — no project content. Edit the hooks to your taste; keep the principle.

> The frontmatter below matches what the Claude Code auto-memory harness emits: a short kebab-case `name:` slug, a one-line `description:`, and `node_type: memory` under `metadata:`. Cross-links use `[[name-slug]]` (the target's `name:`, not its filename). When Claude Code writes a memory itself it also adds bookkeeping fields (e.g. `originSessionId`); hand-authored files only need `name` + `description` + `node_type` + `type`.

---

### `feedback_evidence_over_claims.md`

```markdown
---
name: evidence-over-claims
description: Never assert a result without a captured artifact; no eval-gaming.
metadata:
  node_type: memory
  type: feedback
---

Claims about behavior must be backed by evidence the owner can inspect: command
output, a screenshot, a query result, a captured log. Never say "it works",
"tests pass", or "done" from inference alone — if you didn't run it, say so.

Do not game evaluations: don't weaken a test to make it green, don't assert
"row exists"-style internals as proof of behavior. Tests derive from
business/technical claims and verify behavior at the surface. See
[[completion-ritual]] for the audit that enforces this at "done".
```

---

### `feedback_completion_ritual.md`

```markdown
---
name: completion-ritual
description: Two consecutive clean fresh-context audit rounds before any seal or context-clear.
metadata:
  node_type: memory
  type: feedback
---

Before declaring "done", sealing a milestone, or clearing context, run the
completion ritual: spawn a fresh-context auditor (a new subagent, a second AI,
or a different person) that does NOT know prior verdicts, and have it genuinely
re-audit the work. Any finding resets the count. Exit only on TWO consecutive
clean rounds, each with a fresh reviewer; the first pass is foundational and
uncounted. Use multiple rounds for breadth — a single pass is not an audit.
Pairs with [[evidence-over-claims]] and [[review-gate]].
```

---

### `feedback_review_gate.md`

```markdown
---
name: review-gate
description: Self-review every spec/plan/approach; min 3 iterations, exit on 2 consecutive clean.
metadata:
  node_type: memory
  type: feedback
---

The author owns the review of their own spec, plan, and execution approach —
don't outsource judgment to the owner. Iterate at least 3 times; exit on 2
consecutive clean passes (the 1st pass is foundational and uncounted). Use
fan-out for decomposable review (judge panel, adversarial verify,
loop-until-converged) and a gated chain when steps depend on each other.
Execution is automated once the gate is clean; the owner delegates and
spot-checks via [[completion-ritual]].
```

---

### `feedback_proactive_but_cautious.md`

```markdown
---
name: proactive-but-cautious
description: Run reads/inspects/builds/tests without asking; surface destructive ops first.
metadata:
  node_type: memory
  type: feedback
---

No permission needed to read, inspect, build, or run tests — just do them, but
always understand the effect before running. For destructive or irreversible
operations (deletes, force-push, data migrations, anything that touches shared
state), surface the exact command and get confirmation first. Bias to action on
safe operations; bias to caution on anything you can't undo.
```

---

### `feedback_state_change_currency.md`

```markdown
---
name: state-change-currency
description: After any push/merge/seal/defer/branch, reconcile front-door docs + memory unprompted.
metadata:
  node_type: memory
  type: feedback
---

After any state change — push, merge, seal, defer, new branch — proactively
reconcile the front-door docs (the resume cursor, the roadmap) and any affected
memory for now-stale claims, without being asked. Use drift-proof phrasing.
Refresh the durable handoff so a context-clear is safe immediately. Leave
project history alone — rephrase stale guidance, don't rewrite the past. See
[[doc-funnel]] for which docs are the front door.
```

---

### `feedback_context_handoff.md`

```markdown
---
name: context-handoff
description: No self-meter for context; keep the handoff always-current so a clear is always safe.
metadata:
  node_type: memory
  type: feedback
---

The agent cannot reliably measure its own remaining context. The owner watches
the budget meter. So: keep the durable handoff (the resume cursor + relevant
memory) always current as you work, not at the end — that way clearing context
is safe at any moment. Propose clear-and-resume at heavy seams (after a seal,
before a large new initiative). Pairs with [[state-change-currency]].
```

---

### `reference_doc_funnel.md`

```markdown
---
name: doc-funnel
description: BACKLOG→ROADMAP→NEXT-STEPS→PRD; stable IDs, one canonical home per item.
metadata:
  node_type: memory
  type: reference
---

Documentation flows in one direction:
  BACKLOG (raw ideas) → ROADMAP (sequenced milestones)
  → NEXT-STEPS (the front door: current cursor + safe-resume prompt)
  → PRD (active-increment requirements).

Rules: every item gets a stable ID; each fact has exactly one canonical home;
everywhere else references it by ID (never duplicate the content). A coherence
pass checks cross-artifact consistency whenever a funnel doc changes. Start each
session at NEXT-STEPS. The tool-owned state directory of any planning tool is
NOT part of the funnel and is not hand-curated — see [[tool-owned-state]].
```

---

### `feedback_tool_owned_state.md`

```markdown
---
name: tool-owned-state
description: A planning tool's regenerated state dir is gitignored; the durable trail is your docs + commit history.
metadata:
  node_type: memory
  type: feedback
---

When a planning/automation tool keeps its own state directory, that directory is
the tool's to regenerate — not yours to hand-edit. The tool overwrites it on its
own schedule, so hand edits are futile and invite schema drift. Therefore:

- **Gitignore the tool's state directory.** Don't track it; don't curate it.
- **Keep the durable record in YOUR artifacts** — the docs funnel
  ([[doc-funnel]]) plus commit history. That is the real trail.
- **Commit docs at every milestone boundary**, so the history reflects each
  state change. Pairs with [[state-change-currency]].
```
