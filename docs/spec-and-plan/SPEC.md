# {{FEATURE_NAME}} — Design Spec

<!-- A DESIGN SPEC: what to build and why, settled BEFORE the implementation plan. -->
<!-- It is the source of truth the plan references. Under the Keelwright lifecycle a spec -->
<!-- passes the author's own review gate (iterative self-review to convergence) AND -->
<!-- a coherence audit BEFORE it reaches the owner — the owner reads it async, for -->
<!-- visibility, not as a blocking approval. Cite real files/symbols; verify them -->
<!-- against the live code, never from memory. -->

**Date:** 2026-07-01 · **Branch:** `{{BRANCH}}` (off `{{BASE_BRANCH}}`) · **Status:** {{STATUS}}
<!-- Status examples: brainstorm · spec (decisions settled, implementation-ready) · superseded -->
**Scope owner surface:** {{SCOPE_PATHS}}
<!-- Optional: name the HUB file(s) that serialize writers (Ritual 13). -->
**Hub file(s):** {{HUB_FILES}}

---

## 1. Summary, scope & non-goals

<!-- 2–4 sentences: what this milestone does and the shape of the work. Then two -->
<!-- explicit lists. Non-goals are as important as goals — they prevent scope creep -->
<!-- and tell the reviewer what NOT to flag as missing. -->

{{ONE_PARAGRAPH_SUMMARY}}

**In scope:**
- {{IN_SCOPE_ITEM}}
- {{IN_SCOPE_ITEM}}

**Non-goals / explicitly out of scope:**
- {{OUT_OF_SCOPE_ITEM}}
- {{OUT_OF_SCOPE_ITEM}}
<!-- Call out anything off-limits to edit (vendored/3rd-party) here. -->

**Deferred (named, with enabler):**
<!-- DIFFERENT from non-goals: these are NOT permanently out — they are carried -->
<!-- forward and will land once a named trigger/enabler condition is met. Naming the -->
<!-- enabler is what lets a future session pick the item up at the right moment. -->
- {{DEFERRED_ITEM}} → enabled by {{ENABLER_OR_TRIGGER}}
- {{DEFERRED_ITEM}} → enabled by {{ENABLER_OR_TRIGGER}}
<!-- If nothing is deferred, say "None — no carry-forward items." -->
<!-- Each deferral should also live as an ID in BACKLOG.md (Ritual 14). -->

---

## 2. Context & current state

<!-- The relevant slice of the live system as it is TODAY, verified by reading the -->
<!-- code. What exists, what's missing, what the change builds on. Cite real -->
<!-- files/symbols (e.g. `path/to/file`, a function name) — the reviewer re-checks -->
<!-- these against the live code. -->

{{WHAT_EXISTS_TODAY}}

<!-- Optional: a "Material findings vs. the brief" subsection if reading the code -->
<!-- contradicted the original ask — surface those facts here so the plan is shaped -->
<!-- around reality, not the request. -->

---

## 3. Settled decisions / forks

<!-- The durable record of forks that ARE settled — questions that had real options, -->
<!-- resolved (by the owner or the author) BEFORE this spec went implementation-ready. -->
<!-- Recording them here, with rationale, is what keeps the codebase from silently -->
<!-- contradicting a deliberate call later. These are CLOSED; genuinely-open items -->
<!-- belong in §8 (Open decisions). If a settled fork is later reopened, move it back. -->

| # | Fork / question | Decision (rationale) |
|---|---|---|
| 1 | {{FORK_OR_QUESTION}} | {{DECISION}} — {{WHY}} |
| 2 | {{FORK_OR_QUESTION}} | {{DECISION}} — {{WHY}} |

<!-- If nothing needed settling, say "None — no contested forks." -->

---

## 4. Design

<!-- The actual design. Decisions, not options-still-open (settle forks before the -->
<!-- spec is "implementation-ready"; if a gray-area fork genuinely needs the owner, -->
<!-- mark it and surface it via a real decision point). Use tables/diagrams over -->
<!-- prose. Be concrete: real names, real signatures, real anchors. No placeholders -->
<!-- like "handle errors" — say how. -->

### 4.1 {{ASPECT}}

{{DESIGN_DETAIL}}

### 4.2 {{ASPECT}}

{{DESIGN_DETAIL}}

<!-- Add subsections per aspect: data model, API/contract, UI, control flow, -->
<!-- migration/back-compat, failure modes. -->

---

## 5. Phasing & ordering (if multi-phase)

<!-- If the work splits into phases, justify the ORDER (why this before that). -->
<!-- Include the parallel-vs-serial map (Ritual 13): which files are multiply- -->
<!-- touched (→ serialize), which streams are disjoint (→ parallel-safe). -->

| Phase | Workstreams | Rationale |
|---|---|---|
| **Phase 1** | {{WORK}} | {{WHY_FIRST}} |
| **Phase 2** | {{WORK}} | {{WHY_SECOND}} |

**File-touch / concurrency map:**

| File | Touched by | Concurrency |
|---|---|---|
| {{HUB_FILE}} | {{TASKS}} | **SERIAL** — one writer at a time |
| {{DISJOINT_FILE}} | {{TASKS}} | **PARALLEL-SAFE** — disjoint |

---

## 6. Backward compatibility & risk

<!-- Every change checked against existing callers, tests, config defaults, contracts. -->
<!-- New config has safe defaults. Signature/return-type changes account for EVERY -->
<!-- call site. Name the risks and how the design contains them. -->

- **Compatibility:** {{WHAT_COULD_BREAK_AND_WHY_IT_WONT}}
- **Risks:** {{RISK}} → {{MITIGATION}}
- **Rollback:** {{HOW_TO_REVERT}}

---

## 7. Verification strategy

<!-- HOW the build will be proven, per Keelwright's verification doctrine: tests derive -->
<!-- from claims and verify BEHAVIOR at real surfaces (not internals); UI/behavioral -->
<!-- surfaces get LIVE verification before any "it works" claim; pure-backend gets -->
<!-- tests / direct probes. List the concrete claims to verify, not "add tests". -->

| Claim to verify | Surface | How |
|---|---|---|
| {{BUSINESS_OR_TECHNICAL_CLAIM}} | {{SURFACE}} | {{TEST_OR_LIVE_CHECK}} |
| {{CLAIM}} | {{SURFACE}} | {{HOW}} |

<!-- Note which surfaces require LIVE in-session verification vs. automated tests. -->

---

## 8. Open decisions (for the owner)

<!-- ONLY genuine decision points the rules reserve for the owner (gray-area design -->
<!-- forks, scope/priority calls). Everything else should already be settled in §3/§4. -->
<!-- Resolve these before marking the spec implementation-ready; record the -->
<!-- resolution inline. If none, say "None — all decisions settled." -->

- {{DECISION_NEEDED}} — options: {{A}} / {{B}}. **Resolution:** {{RESOLVED_OR_PENDING}}.

---

## 9. Self-review log (the author owns the gate)

<!-- Record the iterative self-review (min iterations, exit on consecutive clean -->
<!-- passes). Each iteration: what lens was emphasized, what was found, what was -->
<!-- fixed, pass/fail. This log is the EVIDENCE the gate ran — an asserted -->
<!-- "looks good" is not a pass. Convergence = approved-by-default; proceed. -->

| Iteration | Lens emphasis | Findings | Result |
|---|---|---|---|
| 1 (foundational) | {{LENS}} | {{FINDINGS}} | {{fix/clean}} |
| 2 | {{LENS}} | {{FINDINGS}} | {{fix/clean}} |
| 3 | {{LENS}} | {{FINDINGS}} | {{clean}} |

**Outcome:** {{CONVERGED_OR_CONTINUE}} — {{NEXT_STEP}}.
