# Lessons learned — 2026-07-01 v1 (csv2json) SPEC review cadence

The full completion-ritual cadence (core/03-REVIEW-GATES.md) run against a single, small
CLI feature spec — 9 rounds, several independent from-scratch implementations, real
defects found through round 6, then a shift to pure front-door-currency findings in
rounds 7–9. The blockers and fixes that surfaced.

### Exception-handling design (Python stdlib)

1. **Issue:** `csv.reader`'s ragged-row detection, added to reject silent data loss,
   turned out to also reject a harmless trailing/interior blank line in the data region —
   an extremely common real-world CSV shape.
   **Mitigation:** explicitly skip a zero-length row before the width check, distinct
   from rejecting a genuinely short/long row.
   **Lesson:** a hardening rule written for one failure mode (silent data loss) can
   accidentally net an unrelated, harmless case (a blank line loses nothing) — check the
   new rule against adjacent, common inputs, not just the case it was written for.

2. **Issue:** an exception-catalog was rebuilt three separate times (rounds 1, 3, 4) and
   was *still* incomplete each time — `PermissionError`/`NotADirectoryError` (round 3),
   then `csv.Error` (round 4) each slipped through an itemized `except` list that looked
   complete.
   **Mitigation:** replaced itemized `OSError` subclass enumeration with one blanket
   `except OSError as e: ... e.strerror`, and gave `csv.Error` its own dedicated clause
   once discovered it isn't a `ValueError`/`OSError` subclass.
   **Lesson:** an itemized exception list is an open-ended, easy-to-under-enumerate
   surface — for a broad exception family (here, filesystem errors), one blanket handler
   keyed on the family's shared base class is more robust than trying to name every
   subclass in advance.

3. **Issue:** a two-state discriminator (`reading_done`) for choosing an error-message
   prefix silently produced a broken message (`cannot write None: ...`) the moment a
   third real state existed — writing to stdout, not `-o`, can also fail (most commonly
   `BrokenPipeError` from piping into `| head`).
   **Mitigation:** added the third state explicitly, plus a dedicated `BrokenPipeError`
   clause following Python's own documented SIGPIPE idiom (quiet exit, not an error).
   **Lesson:** a boolean discriminator often silently encodes "exactly two states exist"
   — when adding a new state to a design, explicitly re-examine every place a boolean
   flag was used to distinguish "this vs. everything else."

### Review-cadence process

4. **Issue:** the front-door docs (this project keeps three: root `README.md`,
   `docs/README.md`, `docs/NEXT-STEPS.md`) drifted stale for 6 full review rounds while
   attention was on `SPEC.md`'s content — and even the reconcile pass (round 7) missed
   one of the three (round 8 caught it).
   **Mitigation:** reconciled all three in one pass; promoted a carry-forward checklist
   in `docs/PROJECT_RULES.md` naming all three explicitly, so a future reconcile has a
   checklist instead of relying on memory.
   **Lesson:** "reconcile the front-door docs" as a vague category is easy to
   under-execute — name the exact surfaces once, in a durable place, so the sweep is a
   checklist, not a recall exercise.

5. **Issue:** the review log's own "Nth independent implementation" count drifted
   internally inconsistent (3rd → 4th → 6th, skipping a 5th) because it was never
   rigorously tracked, just estimated per-round.
   **Mitigation:** softened the language to avoid asserting a precision that wasn't
   actually being tracked.
   **Lesson:** don't let a review log assert a specific count unless something is
   actually counting — a qualitative claim ("several independent implementations, zero
   defects") is more honest than a precise-sounding number with no ledger behind it.
