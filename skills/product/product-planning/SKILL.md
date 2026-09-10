---
name: product-planning
description: >-
  Plans a product feature until it is ready to spec. Use when
  planning a feature, writing a feature plan, scoping a new
  capability, bounding a grab-bag request, or checking zero
  states, UX copy, user parity, or product analytics.
license: MIT
metadata:
  audience: product
  author: Pranav Prakash
  version: "0.1.0"
---

# Product planning

Turn a proposed feature into a bounded planning brief: who it is
for, what it collides with, how a regular user gets through it,
and how it will be measured.

## When to use

Use when the user wants to plan, scope, or readiness-check a
product feature. Work from the product repo if one is in the
workspace; if not, ask for unseen surfaces and mark those scans
unseen. Do not invent the existing product. Produce the brief in
the conversation. Write a file only if asked.

Don't use for a full PRD, backlog ranking, a time bet, visual
design, or launch comms.

## Workflow

Copy this checklist and work through it in order:

```
Planning Progress:
- [ ] Intention locked (or asked); grab-bag narrowed to one story
- [ ] Boundaries set (appetite, no-gos)
- [ ] Same-realm features listed
- [ ] Impacted features listed
- [ ] Rabbit holes settled, cut, or marked out of bounds
- [ ] Zero states covered
- [ ] Existing vs new user parity checked
- [ ] UX matches existing product; copy, flow, loaders, and API failures pass
- [ ] Analytics inventory done for platforms actually in the product
```

1. **Lock intention.** If the request already states the user, the
   job, the outcome, and the non-goal, restate them and continue. If
   any of those are missing, ask — do not invent a product vision.
   Cap the ask at four questions: who, job-to-be-done, success signal,
   and what is out of scope. Reject grab-bags ("redesign X", "X 2.0")
   until they are one story. Done when you can say the intention in
   two sentences the user would accept. Load
   [references/boundaries.md](references/boundaries.md).

2. **Set boundaries.** Ask how much this is worth, then fit the plan
   to that box — do not estimate a full design backward. Write
   no-gos for what the appetite cannot afford. Keep altitude at
   elements and journeys, not wireframes or a slogan. Done when
   appetite and no-gos are explicit. Load
   [references/boundaries.md](references/boundaries.md).

3. **Scan same-realm features.** Search the product repo (or the
   surfaces the user provided) for capabilities that already do this
   job or sit next to it: routes, settings, flags, help copy, admin
   surfaces. List each with what it already covers. Done when you
   can name overlap, reuse, or a true greenfield. Load
   [references/impact-scan.md](references/impact-scan.md).

4. **Scan impact and name rabbit holes.** List features that will
   change even if they are not the feature: navigation, data other
   screens read, permissions, notifications, billing, shared empty
   states. Then name unknowns that blow scope; settle, cut, or mark
   each out of bounds. Done when every likely blast-radius surface is
   named or marked unseen, and no rabbit hole is left as "we'll see."
   Load [references/impact-scan.md](references/impact-scan.md) and
   [references/boundaries.md](references/boundaries.md).

5. **Walk zero states.** For every new or changed surface, cover the
   first-use and empty cases. Done when no new screen is specified
   only in its happy path. Load
   [references/zero-states.md](references/zero-states.md).

6. **Check user parity.** Existing users and new users must be able
   to reach the same capability the same way, unless a difference is
   called out on purpose. Flag migrations, backfills, "works only on
   a fresh account," and default/flag traps. Done when parity holds
   or each gap has an owner and a reason.

7. **Check UX.** Match patterns and words already in the product.
   Write copy a regular internet user can read once and act on —
   precise verbs for what the product actually does (if it only
   does text chats, do not say "talk"). The workflow itself must
   be understandable in one go. Every API wait needs a visible
   loader; failures keep the user's work and say what to do next.
   Done when inconsistencies, twice-read copy, fuzzy verbs, missing
   loaders, and unhandled API failures are named or fixed.
   Load [references/ux.md](references/ux.md).

8. **Inventory analytics.** Discover which product-analytics
   platforms this product actually uses (Customer.io, PostHog,
   Google Analytics, Datadog, or others). Do not assume a platform
   exists because it is common. Map the feature's journeys to
   events. If a tool can query a connected platform, verify live
   definitions after the code scan; otherwise mark the live check
   unseen. Done when each key action has a planned or existing
   event, or an explicit gap. Load
   [references/analytics.md](references/analytics.md).

9. **Produce** the brief below. **Verify** against the checklist.

## Output

```markdown
# Feature plan: [name]

## Intention
- User:
- Job:
- Outcome:
- Non-goals:

## Boundaries
- Appetite:
- Rabbit holes: (settle / cut / out of bounds)
- No-gos:

## Same-realm features
| Feature | Relationship | Reuse or conflict |

## Impacted features
| Surface | How it changes | Risk if ignored |

## Zero states
| Surface | Empty / first-use | Denied / error | Notes |

## User parity
- Existing users:
- New users:
- Gaps (migration, backfill, flags, defaults):

## UX
- Consistency with existing:
- Copy (one-read, precise):
- One-pass flow:
- Loaders (per API wait):
- API failures:
- Gaps:

## Analytics
- Platforms found in this product:
- Journey → event map:
- Gaps:

## Open questions
- [Only items you could not verify]
```

## Pitfalls

- Treating a vague ask or a grab-bag as a spec — one story first.
- Estimating a full design instead of fitting a solution to an appetite.
- Leaving a rabbit hole as "we'll see."
- Planning only the populated happy path — zero states ship too.
- Designing for new accounts and leaving existing users on an island.
- Shipping a new pattern or a new word for a job the product already has.
- Copy that needs a second read, or a verb the product does not do
  ("talk" for text chat).
- A flow an average internet user cannot follow in one go.
- A call with no loader, or a failure that dumps a raw error or blank screen.
- Inventing analytics platforms the product does not have.
- Claiming a live analytics check when no query tool was available.

## Verification

- [ ] Intention is one story, not a grab-bag
- [ ] Appetite, rabbit holes, and no-gos are filled
- [ ] Same-realm and impacted lists come from the repo or user-provided
      surfaces — not memory
- [ ] Every new surface has at least one zero state
- [ ] Existing and new users can complete the job the same way, or the
      difference is explicit
- [ ] UX matches existing patterns and words, or each break is named
- [ ] New copy is one-read; core flow is understandable in one go
- [ ] Every new API wait has a loader; failures have copy and a next step
- [ ] Analytics list matches platforms actually integrated
- [ ] Brief matches the template; unverified items are in Open questions

## Resources

Load only the file the current step needs:

- [references/boundaries.md](references/boundaries.md) — grab-bags, appetite, no-gos, rabbit holes
- [references/impact-scan.md](references/impact-scan.md) — same-realm overlap and blast radius
- [references/zero-states.md](references/zero-states.md) — empty, denied, and first-use states
- [references/ux.md](references/ux.md) — consistency, copy, flow, loaders, API failures
- [references/analytics.md](references/analytics.md) — platform inventory and event map
