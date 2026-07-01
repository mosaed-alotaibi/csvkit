# PRD — csvkit

<!--
  The Product Requirements Document. Keelwright treats the PRD as a LIVING, AS-BUILT
  document: it describes what the system IS today, grounded in real artifacts
  (file paths, endpoints, tools), not what it might become. Deferred capabilities
  are NOT "unmet requirements" — they live in §9 Future improvements and link out
  to ROADMAP.md / BACKLOG.md.

  Funnel position (see ../../keelwright/core/01-DOC-MODEL.md for the doc model):
    BACKLOG → ROADMAP → NEXT-STEPS → PRD
  The PRD is the right end: the canonical record of current as-built requirements.

  Keep status badges honest: ✅ done · ◑ partial · ⛔ deferred/descoped · 🔒 locked.
-->

**Status:** Living — reflects the **as-built** system.
**Last updated:** 2026-07-01 — <!-- one line: the most recent load-bearing state change -->
**Owner:** mosalotaibi

<!-- If the system exists in more than one as-built shape (e.g. local-dev vs a
     deployed env) that differ in load-bearing ways, say so HERE in one line and
     point at the single canonical reconciliation table (§4.1). Do not scatter the
     deltas across every requirement. -->

> **Scope of this document.** The consolidated, *current* PRD: what the system **is
> today**. It supersedes any earlier proposal/POC doc for current scope.
> Companion docs: [`ROADMAP.md`](ROADMAP.md) (plan + history), [`NEXT-STEPS.md`](NEXT-STEPS.md)
> (resume runbook), [`BACKLOG.md`](BACKLOG.md) (parking lot).

---

## 1. TL;DR

<!-- 3–6 sentences a new engineer can read in 30s: what the product does, who uses
     it, the one defining constraint, and the single proof it works. Name the real
     surfaces (a sign-in, a primary action, the output). No marketing. -->

csvkit is a {{ONE_LINE_PRODUCT_DESCRIPTION}}. A {{PRIMARY_USER}} {{CORE_USER_ACTION}}
and gets {{CORE_OUTPUT_WITH_ITS_KEY_GUARANTEE}}. {{THE_ONE_DEFINING_CONSTRAINT}}.

## 2. Problem & users

<!-- The pain, in concrete terms (what people do by hand today). Name the primary
     user and the deployment target (single-user / single-tenant / multi-tenant). -->

{{WHAT_USERS_DO_THE_HARD_WAY_TODAY}}. **Primary user:** {{PRIMARY_USER_ROLE}}.
**Deployment target:** {{TENANCY_AND_SCALE}}.

## 3. Goals

<!-- The durable goals, each with an honest status. A goal is a property of the
     product, not a task. Keep this to the handful that actually shaped the build. -->

| # | Goal | Status |
|---|---|---|
| G1 | {{GOAL_ONE}} | ✅ |
| G2 | {{GOAL_TWO}} | ◑ |
| G3 | {{GOAL_THREE}} | ⛔ deferred ({{WHY}}) |

## 4. Architecture (as built)

<!-- A small ASCII diagram of the real runtime shape: each tier, its tech as a
     PLACEHOLDER, the port/surface, and the data flow arrows. Mark any off-limits /
     vendored component explicitly. Point at a fuller ARCHITECTURE doc if one exists. -->

```
{{CLIENT_TIER}} — {{WEB_FRAMEWORK}} ({{CLIENT_PORT}})   ── {{CLIENT_RESPONSIBILITIES}}
   │  {{TRANSPORT_OR_SESSION_MECHANISM}}
   ▼
{{SERVICE_TIER}} — {{BACKEND_FRAMEWORK}} / {{DATASTORE}} ({{SERVICE_PORT}})
   │   {{SERVICE_RESPONSIBILITIES}}
   ▼
{{INTEGRATION_TIER}}  ── {{EXTERNAL_SYSTEM_OR_CONNECTOR}}
   ▼
{{COMPUTE_OR_MODEL_TIER}} ── {{WHAT_RUNS_HERE}}
```

{{DATASTORE}} stores {{KEY_ENTITIES}}. Full detail: {{LINK_TO_ARCHITECTURE_DOC}}.

### 4.1 Environment split — the as-built reconciliation (canonical)

<!-- ONLY if the system has >1 as-built shape. This table is the single source of
     truth for the deltas; every environment-specific claim below should be read
     against it. Delete this subsection if there is only one shape. -->

| Dimension | {{ENV_A}} (the FRs below) | {{ENV_B}} |
|---|---|---|
| {{DIMENSION_1}} | {{ENV_A_VALUE}} | {{ENV_B_VALUE}} |
| {{DIMENSION_2}} | {{ENV_A_VALUE}} | {{ENV_B_VALUE}} |

Authoritative {{ENV_B}} config = {{POINTER_TO_DEPLOYED_CONFIG}}; current status = {{POINTER_TO_STATUS_DOC}}.

## 5. Functional requirements (implemented)

<!-- Group FRs by area. Each FR: a stable ID (FR1, FR2, …), a short title, the real
     artifact it lives in (path / endpoint / tool name), and what it actually does.
     IDs are stable and never reused. Mark deferred FRs ⛔ inline and point at §9. -->

### 5.1 {{AREA_ONE}}
- **FR1 — {{TITLE}}** (`{{ARTIFACT_PATH_OR_ENDPOINT}}`): {{WHAT_IT_DOES}}.
- **FR2 — {{TITLE}}** *(⛔ deferred — {{WHY}}; see §9)*: {{WHAT_IT_WOULD_DO}}.

### 5.2 {{AREA_TWO}}
- **FR3 — {{TITLE}}** (`{{ARTIFACT}}`): {{WHAT_IT_DOES}}.

### 5.3 {{AREA_THREE}}
- **FR4 — {{TITLE}}** (`{{ARTIFACT}}`): {{WHAT_IT_DOES}}.

<!-- For any area with a notable history (e.g. an audit, a security finding, a
     reversed decision), add a short blockquote note here recording the finding,
     what was verified, and what remediated it — with the evidence pointer. -->

## 6. Non-functional requirements

<!-- Cross-cutting properties with honest status. Each NFR: a property + how it's
     held + status. Use ◑ when it's met in practice but not formally measured. -->

| # | Requirement | Status |
|---|---|---|
| NFR1 | {{NFR_ONE}} | ✅ |
| NFR2 | {{NFR_TWO}} | ◑ {{CAVEAT}} |
| NFR3 | {{NFR_THREE}} | ✅ |

## 7. Data / integrations (current)

<!-- Each live data source / external integration: identity/auth model, scope
     (read-only vs read-write), and the real endpoint or dataset it touches. -->

- **{{SOURCE_ONE}}** — {{WHAT_AND_WHERE}}. Auth: {{IDENTITY_MODEL}}. Access: {{READ_ONLY_OR_RW}}.
- **{{SOURCE_TWO}}** — {{WHAT_AND_WHERE}}. Auth: {{IDENTITY_MODEL}}.

## 8. Success metrics (as built)

<!-- The north-star bar and the ACTUAL measured result. Tie every metric to a
     reproducible check. If a deliverable gate was passed, record when + how. -->

- **North star:** {{TARGET}}. **Actual:** {{MEASURED_RESULT}}.
- **{{DELIVERABLE_GATE}}:** {{PASS_CRITERIA}} — {{PASSED_WHEN}}.

## 9. Future improvements (deferred — the roadmap)

<!-- NOT gaps. Intentional next steps, each with a clear trigger. This is the
     capability catalog; ROADMAP.md owns the ORDER and BACKLOG.md owns the detail.
     Reference backlog items by ID — do not restate their detail here. -->

> **Prioritization & milestone framing live in [`ROADMAP.md`](ROADMAP.md); item detail
> lives in [`BACKLOG.md`](BACKLOG.md) by ID.** This table is the *capability catalog*.

| Area | Improvement | Trigger / notes |
|---|---|---|
| {{AREA}} | {{IMPROVEMENT}} ({{BL-ID}}) | {{WHEN_IT_MATTERS}} |
| {{AREA}} | {{IMPROVEMENT}} ({{BL-ID}}) | {{WHEN_IT_MATTERS}} |

## 10. Out of scope (today)

<!-- Deliberate non-goals for the current shape. State them so they aren't mistaken
     for omissions. -->

{{NON_GOAL_ONE}}; {{NON_GOAL_TWO}}; {{NON_GOAL_THREE}}.

## 11. Source-of-truth map

<!-- One line per doc, naming which doc is canonical for what. The PRD is canonical
     for current as-built requirements. Point at the docs front door if you keep one. -->

The canonical doc map lives in {{DOCS_FRONT_DOOR}}. This PRD is canonical for
**current as-built requirements**; [`ROADMAP.md`](ROADMAP.md) for the plan + history;
[`NEXT-STEPS.md`](NEXT-STEPS.md) for resume state; [`BACKLOG.md`](BACKLOG.md) for the parking lot.
