# Lessons learned — 2026-07-01 v1 (csv2json) SPEC review cadence

The full completion-ritual cadence (core/03-REVIEW-GATES.md) run against a single, small
CLI feature spec — 12 rounds, several independent from-scratch implementations, and
real defects found as late as round 10 before rounds 11–12 converged cleanly. The
blockers and fixes that surfaced.

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

6. **Issue:** the carry-forward checklist added in round 8 (naming all three
   front-door surfaces explicitly, specifically to stop this from recurring) was
   itself violated by round 9's own commit — `docs/NEXT-STEPS.md` was the one surface
   not touched, even though the other two were reconciled correctly. A written
   checklist did not, by itself, guarantee the sweep actually happened.
   **Mitigation:** reconciled `docs/NEXT-STEPS.md` in round 10; no further process
   change beyond re-emphasizing the checklist, since the checklist's content was
   already correct — the miss was execution, not a missing rule.
   **Lesson:** a carry-forward checklist reduces the *chance* of a miss; it doesn't
   eliminate it. The real backstop is the review cadence itself catching what a
   single pass misses — which is exactly what happened here. Don't treat "we wrote
   a checklist for this" as proof the class of bug is closed.

7. **Issue:** the `BrokenPipeError` fix (lesson 3 above) was itself incomplete —
   `sys.stdout.write()` doesn't reliably raise `BrokenPipeError` for ordinary-sized
   output (Python buffers stdout; the exception only surfaces at interpreter
   shutdown, outside any `except` block, leaking "Exception ignored" + exit 120).
   The bug survived 9 rounds because every test of it used a large fixture (which
   happens to force a synchronous OS-level write), never an ordinary small one.
   **Mitigation:** added `sys.stdout.flush()` immediately after the write, inside
   the `try` — the exact line the cited Python SIGPIPE recipe uses and which the
   spec's prose had omitted despite citing the recipe; added a §7 test using a
   *small* fixture specifically, not just a large one.
   **Lesson:** a verification test's *choice of fixture size/shape* can silently
   avoid the exact code path a fix depends on. When citing an external "official"
   recipe, transcribe **every** line of it, not just the parts that look load-bearing
   at a glance — and test the common case (small input), not just the case that's
   easiest to make deterministic (large input).
