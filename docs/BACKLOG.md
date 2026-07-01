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
| **BL-001** | `json2csv` (reverse of csv2json) | feature | parked | v1 only ships one direction (csv→json); a real second direction hasn't been needed yet. | A new `csvkit/convert.py` function `json_to_csv_rows` + a `json2csv` subcommand in `cli.py`, mirroring csv2json's structure (module layout, error handling, CLI contract). | `docs/spec-and-plan/SPEC.md` §1 |
| **BL-002** | `--infer-types` flag | enhancement | parked | v1 keeps every value a JSON string (safe default — e.g. avoids mangling a zip code's leading zero); type inference is ambiguous and deferred until a real consumer needs typed JSON. | An opt-in flag on `csv2json` that attempts int → float → bool → string coercion per cell, strictly additive (default behavior unchanged). | `docs/spec-and-plan/SPEC.md` §1, §3 decision 3 |
| **BL-003** | `--delimiter` flag (semicolon/tab) | enhancement | parked | v1 is comma-only; no real non-comma input file has shown up yet. | Pass a custom `delimiter=` through to `csv.reader`/`csv.writer`; stdlib already supports this natively — small change once needed. | `docs/spec-and-plan/SPEC.md` §1 |
| **BL-004** | `--no-header` mode | enhancement | parked | v1 always assumes row 1 is the header; no real headerless input file has shown up yet. | Output would need synthetic keys (e.g. `col1`, `col2`, ...) instead of real header names; needs its own design pass for key-naming. | `docs/spec-and-plan/SPEC.md` §1 |
| **BL-005** | pip-installable packaging | enhancement | parked | v1 runs via `python3 -m csvkit`, which needs no packaging step; no use outside this checkout exists yet. | Add `pyproject.toml` with a console-script entry point (`csvkit = csvkit.cli:main`) once the tool is actually used from outside this repo. | `docs/spec-and-plan/SPEC.md` §1 |
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
