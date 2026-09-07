# Documentation check

Load during the documentation step. Do not skip internal docs because the change "was small."

## Where to write

Search the product/engineering repo for the existing docs home, in this order. Use the first one that exists. Do not invent a second tree.

1. A `docs/`, `wiki/`, or `handbook/` directory
2. GitHub wiki or equivalent linked from the README
3. Architecture / feature notes already next to the code (`docs/features/`, `adr/`)
4. README / AGENTS.md only if that is genuinely where this kind of change is recorded

Update the existing page for this feature when one exists. Otherwise add a page and link it from the parent index or README docs section.

## User-facing vs internal

**Internal — always.** Engineers, support, and future-you need a current page for what is in the tree now.

**User-facing — only when a person outside the team can see the change.** Update help, changelog, in-app copy docs, public API reference, or customer-facing README sections when any of these moved:

- User-visible behavior, copy, or empty/error states
- Settings, permissions, pricing/plan gates, or onboarding
- Public API, webhook, or SDK contract
- Something support will be asked about

Skip user-facing docs when the change is tests, refactors, logging, internal APIs, infra, or bugfixes with no user-visible difference. Write the skip reason in the Double Check report. "I forgot" is not a reason.

## Wiki page shape

Write a wiki page, not a commit summary. Every internal page uses this shape. Drop a section only when it truly does not apply; do not drop **What shipped**, **Why**, or **Impact**.

```markdown
# [Feature or change name]

## What shipped
[What a reader can do now, or what the system does now, in present tense.
Not a file list.]

## Why
[The problem or request this answers. One short paragraph.]

## Impact
- Users: [who feels it, or "none — internal only"]
- Systems: [services, tables, queues, flags, jobs that changed]
- Adjacent features: [what else now behaves differently]

## How it works
[The current design: entry points, main flow, important contracts.
Link code paths; do not paste the diff.]

## How to operate
[How to verify it, which flags/env/config it needs, how to turn it off,
what to watch if it breaks.]

## Limits and follow-ups
[Known gaps, out-of-scope pieces, planned follow-up. Empty if none.]
```

User-facing updates, when required, stay in the user-facing voice of that surface (help article, changelog, API doc). They still need what changed, why it matters to the reader, and what to do. They do not need the internal "How it works" section.

## Done when

- Internal page exists and matches the change that is about to be called done
- What / why / impact are specific enough that someone who did not write the code can brief from the page
- User-facing docs are updated, or the skip reason is recorded
- Parent index / related pages point at the new or updated page
