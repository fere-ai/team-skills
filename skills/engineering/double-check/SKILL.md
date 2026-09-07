---
name: double-check
description: >-
  Double-checks engineering work before it ships. Use when the user says
  double check, double-check, or asks to verify work, docs, or impact
  before merge or launch.
license: MIT
metadata:
  audience: engineering
  author: Pranav Prakash
  version: "0.1.0"
---

# Double Check

Before declaring a change complete, verify it against five dimensions and eliminate three failure modes. Do not skip this because the change "looked simple" — simple changes silently break callers most often.

## The five checks

1. **Upstream + downstream logic, flow, and contract**
   - Upstream: every caller/producer that feeds this code (function args, API request shape, DB row, queue message, prior pipeline step). Did you change a signature, return type, schema, status code, or event payload that a caller relies on?
   - Downstream: every consumer of this code's output (callers, deserializers, other services, UI components, DB writes, published events). Do they still receive what they expect?
   - Contract: types/interfaces, API request/response shapes, DB schema, RabbitMQ message schema, function signatures — grep for all call sites and confirm each still compiles/type-checks logically, not just the one you edited.

2. **Sad paths + happy paths**
   - Happy path: the primary intended flow with valid input.
   - Sad paths: invalid/missing input, timeouts, network/DB errors, empty results, permission denial, partial failure, retries, concurrent access, unicode/edge-case data. For each new or touched branch, ask "what happens when this fails?" and confirm it's handled (not just that it doesn't crash on the happy path).

3. **No regression**
   - Diff your change against what existed before: does prior behavior other callers depended on still hold?
   - Re-run or reason through existing tests covering the touched area. If none exist, that itself is a gap worth flagging.
   - Check sibling/related code paths that share the function, config, or component you touched.

4. **Intention & product goals**
   - Re-read the original ask. Does the change actually solve it, or a narrower/adjacent version of it?
   - Check for scope creep or scope gaps: did you do more or less than intended?
   - If the codebase has product/architecture docs (AGENTS.md, CLAUDE.md, README), confirm the change is consistent with stated conventions and goals.

5. **Documentation**
   - Internal docs: always update. Write or refresh a wiki-style page for what shipped. Find the repo's existing docs/wiki tree and update it there — do not start a parallel docs pile.
   - User-facing docs: update only when a user, operator-customer, or public API consumer can see the change (behavior, copy, settings, permissions, help, changelog, public API). If they cannot, skip and state why.
   - A page that only restates the diff is not done. It must say what shipped, why, and what impact it has. Load [references/docs.md](references/docs.md) for the page shape and the user-facing decision.

## The three failure modes to eliminate

- **Loose ends**: TODOs left unresolved, unhandled error branches, unused/dead parameters introduced by the change, missing config/env examples the change now requires (e.g. new env var not added to `.env.local.example`), skipped internal docs, skipped user-facing docs when users can see the change, follow-up work silently assumed but not done.
- **Dead ends**: code paths that can never be reached, imports/exports left dangling, old code left behind that's now unused (feature flags, deprecated functions, orphaned files), a caller that still points at the old behavior/signature.
- **Regressions**: anything that used to work and no longer does — re-check this explicitly, don't just assume it because "the new code is correct in isolation."

## Workflow

Copy this checklist and work through it for the current change set (use `git diff`/`git status` to enumerate touched files):

```
Verification Progress:
- [ ] Enumerated all changed files/functions/endpoints
- [ ] Traced upstream callers of each changed contract
- [ ] Traced downstream consumers of each changed contract
- [ ] Checked at least one sad path per new/changed branch
- [ ] Confirmed happy path still works end-to-end
- [ ] Compared against pre-change behavior for regressions
- [ ] Re-read original request/goal and confirmed full + correct scope
- [ ] Internal wiki page written or updated (what / why / impact)
- [ ] User-facing docs updated, or skip reason recorded
- [ ] Searched for loose ends (TODOs, unhandled branches, missing config/docs)
- [ ] Searched for dead ends (unreachable code, stale callers, orphaned code)
- [ ] Ran relevant tests/lints; fixed or explained any failures
```

**Step 1 — Enumerate the blast radius.** Run `git diff` / `git status` (or list edited files if not in git) to get the exact set of changed files, functions, endpoints, schemas, or event names.

**Step 2 — Trace contracts.** For each changed function signature, API route, DB column, or message schema, search the codebase (grep) for all call sites/consumers. Read each one — don't assume it's fine.

**Step 3 — Walk the paths.** For each changed branch of logic, explicitly state (to yourself or in your response) the happy path and at least one sad path, and confirm both are handled.

**Step 4 — Regression pass.** Ask: "what worked before this change that might not work now?" Check related/sibling code, not just the lines you touched.

**Step 5 — Intent check.** Re-read the user's original request. Confirm the change fully satisfies it — no more, no less — and aligns with any documented conventions/goals in the repo (AGENTS.md/CLAUDE.md/README).

**Step 6 — Documentation.** Load [references/docs.md](references/docs.md). Locate the existing internal wiki/docs tree. Update or add the wiki page (always). Decide user-facing docs: update them, or record why they are not needed. Link the new/updated page from the parent index if one exists.

**Step 7 — Sweep for loose/dead ends.** Grep for TODO/FIXME you introduced, unused imports/exports, unreachable branches, and stale references to old behavior.

**Step 8 — Run checks.** Execute relevant tests/linters for the touched area. If tests don't exist for the changed logic, say so explicitly rather than silently skipping verification.

## Reporting

When you finish, state plainly which of the five checks and three failure modes you verified, where the internal wiki page lives, and whether user-facing docs were updated or skipped (with the reason). Flag anything you could not fully verify (e.g. no test coverage existed, a downstream service you can't run locally). Do not claim "done" without having walked through this list.