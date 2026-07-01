# csvkit — As-Built Scope for QA

<!-- The HONEST testing scope. A trimmed version of PRD.md covering ONLY what is -->
<!-- actually implemented and deployable today. Its job: let QA plan tests AND -->
<!-- avoid filing bugs against intentionally-deferred or mock surfaces. -->
<!-- Where this doc and PRD.md differ, THIS doc wins for what is testable today. -->

**Purpose:** the **QA testing scope** — a trimmed, honest version of [`PRD.md`](PRD.md)
covering **only what is actually implemented and deployable today**. Use it to plan
tests, and to avoid raising bugs against features that are intentionally deferred or
are mock UI.
**Derived:** from [`PRD.md`](PRD.md), audited against the codebase on 2026-07-01.
**Audience:** QA.

---

## 0. Read this first — what the product *is* (and isn't)

<!-- A plain-language paragraph + a one-line mental model. Set expectations before -->
<!-- any table. State the headline feature that is NOT yet real, if there is one. -->

csvkit is **{{ONE_LINE_WHAT_IT_IS}}**. The deployed slice does:

<!-- Bullet the genuinely-working capabilities, plainly. -->
- {{CAPABILITY_1}}
- {{CAPABILITY_2}}
- {{CAPABILITY_3}}

**It does NOT (yet) do:** {{HEADLINE_FEATURE_NOT_YET_REAL}} — see §3. Also note:
{{DEPLOYED_VS_INTENDED_DIFFERENCES}} (e.g. the deployed {{COMPONENT}} differs from
what the PRD describes).

> **One-line mental model for QA:** *{{MENTAL_MODEL_ONE_LINER}}.*

---

## 1. Test environments

<!-- One row per environment. Be explicit about what each CAN and CANNOT test. -->

| Environment | Auth | What it lets you test | What it can't |
|---|---|---|---|
| **{{ENV_LOCAL}}** | {{LOCAL_AUTH}} | {{LOCAL_CAN_TEST}} | {{LOCAL_CANNOT}} |
| **{{ENV_DEPLOYED}}** | {{DEPLOYED_AUTH}} | {{DEPLOYED_CAN_TEST}} | {{DEPLOYED_CANNOT}} |

<!-- Optional: note how to exercise a surface without a live dependency -->
<!-- (e.g. crafted fixtures, a stub mode, recorded responses). -->

---

## 2. ✅ TESTABLE — implemented features

<!-- Group by area. One table per area. -->
<!-- Status legend: ✓ implemented · ◐ implemented but depends on a live prerequisite. -->

Status legend: **✓** implemented · **◐** implemented but depends on a live prerequisite.

### 2.1 {{AREA_1}}

| Feature | Where | How to test / what to verify | Caveat |
|---|---|---|---|
| {{FEATURE}} | {{ENV}} | {{HOW_TO_VERIFY}} | {{CAVEAT}} |
| {{FEATURE}} ◐ | {{ENV}} | {{HOW_TO_VERIFY}} | {{LIVE_PREREQ}} |

### 2.2 {{AREA_2}}

| Feature | Where | Verify | Caveat |
|---|---|---|---|
| {{FEATURE}} ✓ | {{ENV}} | {{VERIFY}} | {{CAVEAT}} |

<!-- Add more areas as needed: e.g. core flow, persistence, i18n/theming, -->
<!-- backend ops/security (the last is mostly invisible to UI but matters to QA-eng). -->

---

## 3. 🕒 NOT YET IMPLEMENTED / DEFERRED — do **not** file bugs

<!-- The explicit "don't waste time here" list. Reference PRD item IDs. -->

| PRD item | Why it's not here |
|---|---|
| {{PRD_ITEM}} | {{WHY_DEFERRED}} |
| {{PRD_ITEM}} | {{WHY_DEFERRED}} |

---

## 4. ⛔ MOCK / DECORATIVE — present in the UI but **NOT real**; do not test as functional

<!-- Surfaces that LOOK functional but are placeholder/static. The most -->
<!-- common source of false-positive bug reports. Be specific about the reality. -->

| Surface | Reality |
|---|---|
| {{MOCK_SURFACE}} | {{WHAT_IT_ACTUALLY_IS}} (e.g. static/hardcoded; labeled placeholder; no backend wiring) |
| {{MOCK_SURFACE}} | {{WHAT_IT_ACTUALLY_IS}} |

---

## 5. ⚠️ Known limitations & caveats QA should know

<!-- Real, accepted limitations: known races, soft vs hard deletes, settings -->
<!-- that are UI-only, security primitives that exist but are not yet wired, etc. -->
<!-- Flag the difference between "broken" and "intentionally limited". -->

- **{{LIMITATION}}** — {{DETAIL_AND_WHEN_TO_FLAG}}.
- **{{LIMITATION}}** — {{DETAIL}}.
- **{{LIMITATION}}** — {{DETAIL}}.

---

## 6. Suggested QA entry points (smoke path)

<!-- A short ordered happy-path smoke that exercises the real, testable surfaces. -->

1. **{{STEP}}** → {{EXPECTED}}.
2. **{{STEP}}** → {{EXPECTED}}.
3. **{{STEP}}** → {{EXPECTED}}.
4. **Negative/scope** → confirm the mock surfaces (§4) read as demo, and that the
   deferred features (§3) do not appear (expected).

*Questions on intended behavior should reference [`PRD.md`](PRD.md) (full intent)
vs this doc (as-built). Where they differ, this doc wins for what's testable today.*
