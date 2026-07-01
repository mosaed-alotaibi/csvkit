# Lessons learned — csvkit

<!-- The index for the per-session lessons-learned log (Keelwright Ritual 12). -->
<!-- One dated file per session: YYYY-MM-DD-<topic>.md. Newest entries link here. -->
<!-- This file is just the index + the ritual reminder; the lessons live in -->
<!-- the dated entry files (use _ENTRY_TEMPLATE.md as the skeleton). -->

Per-session lessons-learned log — concise issues / mitigations / lessons captured
at session end (see [`../PROJECT_RULES.md`](../PROJECT_RULES.md), Lessons-learned
ritual). One dated file per session: `YYYY-MM-DD-<topic>.md`.

---

## The ritual (one pass per session)

Before wrapping a session (and ahead of the pre-done confirmation ritual):

1. Run **one genuine pass**: did anything this session reveal a non-obvious
   gotcha — infra, auth, process, tooling, local dev, or code?
2. **If yes →** append to a dated file `YYYY-MM-DD-<topic>.md` (copy
   [`_ENTRY_TEMPLATE.md`](_ENTRY_TEMPLATE.md)). Group by area; for each issue,
   three one-liners: **Issue · Mitigation · Lesson.** Keep it concise and
   direct — no fluff.
3. **If nothing notable surfaced →** the pass **passes**; note "no notable
   issues" or skip. Do **not** manufacture entries.
4. Add a link to the new file in the index below, then commit it with the
   session's normal docs commit.

**Why:** integration/deployment sessions surface easy-to-forget gotchas
(ordering, exact config values, naming-boundary traps, scoping). Capturing them
while fresh turns one painful debug into a durable checklist for the next
environment and the next engineer.

---

## Index (newest first)

<!-- Add one line per session entry, most recent at the top. -->

- [2026-07-01 — v1 implementation and seal](2026-07-01-v1-implementation-and-seal.md)
- [2026-07-01 — v1 (csv2json) SPEC review cadence](2026-07-01-spec-review-cadence.md)
<!-- - [YYYY-MM-DD — <topic>](YYYY-MM-DD-<topic-slug>.md) -->
