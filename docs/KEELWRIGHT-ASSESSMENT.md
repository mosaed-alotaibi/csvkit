# Keelwright dogfood assessment — csvkit v1

**Date:** 2026-07-01  
**Trial:** start a new project with `keel init`, then run brainstorm → spec → plan →
test-first execution → live verification → completion review.  
**Boundary:** this assessment belongs to the dogfood project. The Keelwright source
repository was not modified.

## Verdict

Keelwright is a strong quality methodology with a weak proportionality story in its
current form. It made a tiny CLI substantially safer and more explainable, and it found
defects that an ordinary “write code, run tests” loop would probably have shipped.
But the same trial also demonstrated that its default ceremony can dominate the work:
the specification took 12 review rounds before convergence, the plan took 6, and the
generated documentation surface needed repeated cleanup and synchronization.

My judgment: **valuable for AI-heavy, high-risk, or handoff-sensitive work; too heavy as
the default for a small low-risk utility until profiles and automation reduce the
ceremony.** I would adopt it selectively today, and broadly after the onboarding and
risk-scaling improvements below.

## Scorecard

| Dimension | Score | What the trial showed |
|---|---:|---|
| Defect prevention | 5/5 | Review and live verification exposed silent data-loss cases, encoding/newline corruption, exception leaks, broken-pipe shutdown noise, stale handoffs, and the final `-o ""` truthiness bug. |
| Evidence quality | 5/5 | Claims ended with exact tests, mutation checks, real files, stdout/stderr, exit codes, and a durable ledger. |
| Resume safety | 4/5 | NEXT-STEPS and the funnel make cold continuation unusually clear, but keeping the mirrors current repeatedly failed without manual sweeps. |
| Initial onboarding | 2/5 | `keel init` worked, but the command was not on PATH, the core path guess was wrong for the actual checkout name, and root README was not scaffolded. |
| Proportionality | 1/5 | Twelve spec rounds for a tiny stdlib CLI is difficult to justify as a universal default, even though the rounds found real defects. |
| Automation | 2/5 | The method says exactly what to verify, but placeholder cleanup, link checks, front-door currency, review ledger maintenance, and status checks remain manual. |
| Overall adoption readiness | 3/5 | Serious and useful, but best used by disciplined teams willing to pay the process cost. |

## What worked unusually well

1. **“Evidence over claims” changed the result.** Real-file tests found CRLF and BOM
   behavior that in-memory tests would miss. Small-payload pipe testing found a Python
   buffering defect that large fixtures accidentally hid.
2. **The doc funnel made context recoverable.** BACKLOG → ROADMAP → NEXT-STEPS → PRD
   separates ideas, sequence, live cursor, and as-built truth cleanly. A stranger can
   reconstruct the project without this conversation.
3. **Repeated adversarial lenses prevented shallow convergence.** Later passes checked
   different failure classes instead of running one checklist three times.
4. **Test effectiveness became an explicit deliverable.** Mutation checks proved that
   critical tests detect real regressions; “39 passed” was not accepted by itself.
5. **The methodology dogfooded honestly.** Its own state-currency rule repeatedly caught
   stale generated docs, and those misses became durable lessons instead of being hidden.

## Where the experience fought the user

1. **The default unit of process is too large.** A small CLI inherited a substantial
   document suite, 16 standing rituals, full-cadence gates, review ledgers, and repeated
   front-door reconciliation. Quality rose, but time-to-value became hard to see.
2. **Initialization assumes local topology.** The generated adoption links guessed a
   sibling checkout named `keelwright`; the real checkout remained named `keel`. The
   project now contains absolute machine-specific links, so a clone elsewhere cannot
   resolve its methodology references.
3. **The scaffold contains “future-shaped” content too early.** Guides, archive
   references, lessons templates, adapters, PRD, QA, wiring, roadmap, backlog, and
   resume machinery all arrive before the project earns most of them. Visible template
   residue and dead references are predictable outcomes.
4. **The root README gap weakens first contact.** The docs map declares root README the
   onboarding source of truth, but init did not create it. That is a provision-before-
   reference mismatch at the most important surface.
5. **Currency is a principle without enough tooling.** Three front doors and several
   mirrored state facts repeatedly drifted. A checklist helped, but did not enforce it.
6. **Strict fresh-context review depends on tool availability.** The method requires
   independent reviewers, yet there is no built-in fallback or explicit “qualified
   convergence” mode when agents are unavailable. This implementation seal records that
   limitation instead of pretending compliance.

## Recommended product changes

Ordered by adoption impact:

1. Add `keel init --profile minimal|standard|high-assurance` and make `standard` the
   practical default. Reserve mandatory full cadence at every seam for high assurance.
2. Scaffold a concise root README with the exact first command, test command, docs link,
   and current project state.
3. Replace guessed relative core paths with a portable reference: vendored/versioned
   methodology snapshot, configured install path, or marker-based discovery.
4. Install only the docs a profile needs. Create guides/archive/QA/wiring artifacts when
   a real lifecycle event first requires them.
5. Add `keel doctor` to detect unresolved placeholders, dead links, missing referenced
   resources, stale clone/path assumptions, and disagreement among the three front doors.
6. Add `keel status` for the current cursor and `keel audit` for tests, repo state,
   placeholders, links, and completion-ledger checks.
7. Make review cadence risk-adaptive. Keep the 3-round/2-clean rule for high-leverage or
   high-risk artifacts; allow a one-pass light gate for tiny reversible changes unless a
   finding escalates them.
8. Store review findings in a small structured ledger rather than embedding long logs in
   the spec. Let tooling compute streaks and render summaries.
9. Automate state-change reconciliation: define front doors once in config, then have a
   check fail when their state markers disagree.
10. Ship adapter conformance tests and a documented local fallback when fresh reviewer
    agents are unavailable.

## Would I use it again?

Yes—with a consciously chosen assurance level. For migrations, release tooling,
security-sensitive integrations, AI-generated infrastructure, or work that must survive
frequent context resets, the discipline is worth it. For a one-file script or a tiny
reversible feature, I would use the philosophy and a minimal profile, not the entire
default ceremony.
