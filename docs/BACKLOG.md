# Backlog — csvkit

<!--
  The parking lot. Human-owned, committed under docs/, ID-stable. This is the LEFT
  end of the doc funnel and the one canonical home for every deferred idea and every
  honestly-recorded removal.

  Funnel position: BACKLOG → ROADMAP → NEXT-STEPS → PRD.
  ROADMAP pulls prioritized items from here; PRD §9 catalogs deferred capability by
  reference. No other doc restates a backlog item's detail — they reference it by ID.
-->

> **Human-owned · committed under `docs/` · ID-stable.** This is the parking lot for
> deferred ideas and honestly-recorded removals. It is the **left end of the doc
> funnel** (`BACKLOG → ROADMAP → NEXT-STEPS → PRD`).
>
> - **One canonical location per item:** each item lives here once, under a stable
>   `BL-NNN` ID. Other docs reference items **by ID** and never restate the detail.
>   IDs are **never reused or renumbered**.
> - **Distinct from any tool-owned state directory:** a planning/automation tool may
>   keep its own gitignored backlog — that is tool-owned, never hand-curated. This
>   `BACKLOG.md` is its human-owned counterpart and the source of truth for the team.
>
> **Schema:** ID · title · type (`feature` | `enhancement` | `removed-deferred`) ·
> status (`parked` | `planned` | `in-progress` | `done` | `dropped`) · why ·
> future-context · source/links.

| ID | Title | Type | Status | Why | Future context | Source |
|---|---|---|---|---|---|---|
<!-- Add rows below. Keep IDs sequential and permanent. Example row (commented out): -->
<!--
| **BL-001** | {{SHORT_TITLE}} | {{feature \| enhancement \| removed-deferred}} | {{parked \| planned \| in-progress \| done \| dropped}} | {{WHY_IT_IS_HERE — for removed-deferred, what was removed and why; for features, the gap}} | {{WHAT_DOING_IT_LATER_LOOKS_LIKE — concrete enough to act on cold}} | {{LINKS — spec section, file path, the milestone/lesson that surfaced it}} |
-->

<!-- Guidance for filling rows:
     - type `removed-deferred`: something working/inert that was REMOVED in a milestone
       and parked for possible return. Record what + why + the revival shape.
     - type `feature` / `enhancement`: not-yet-built work. Record the gap + the
       concrete future shape so a future session can act without this conversation.
     - status `dropped`: an item explicitly killed (keep the row for the trail; say why).
     - Source is mandatory: link the spec/lesson/file that justifies the item. -->

> **Not backlogged (intentional):** {{THINGS_REMOVED_OR_DROPPED_ON_PURPOSE_WITH_NO_REVIVAL_PATH}}.
> Recording these as backlog items would imply a revival path that doesn't exist, so
> they live here only as an explicit note — not as `BL-NNN` rows.
