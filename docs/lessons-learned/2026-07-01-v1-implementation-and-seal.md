# Lessons learned — 2026-07-01 v1 implementation and seal

### CLI edge semantics

1. **Issue:** `if args.output:` collapsed two distinct states—no `-o` option (`None`)
   and an explicitly supplied empty path (`""`)—so `-o ""` silently wrote to stdout.
   **Mitigation:** test option presence with `args.output is not None` and add a real CLI
   regression test that first demonstrated the incorrect exit 0.
   **Lesson:** optional string arguments are often three-state values (absent, empty,
   non-empty); truthiness is not a safe presence check when the empty value has meaning.

### Review evidence

2. **Issue:** a green suite alone did not show whether its highest-value tests could
   detect the regressions they claimed to prevent.
   **Mitigation:** temporarily removed the stdout flush, newline preservation, and
   duplicate-header guard one at a time; each targeted test failed for the expected
   reason, then the exact code was restored and the full suite rerun.
   **Lesson:** a small, reversible mutation audit gives stronger test-effectiveness
   evidence than test counts or coverage percentages alone.

### Methodology adoption

3. **Issue:** init produced several project-irrelevant or not-yet-real references
   (browser verification, guide row, archive index) that survived until completion.
   **Mitigation:** remove live placeholder rows and make project-specific verification
   instructions name the real CLI surface.
   **Lesson:** scaffolding should provision the smallest immediately true system; future
   structure is safer when generated on demand than when installed as optimistic prose.
