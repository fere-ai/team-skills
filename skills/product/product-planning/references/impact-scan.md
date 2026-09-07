# Same-realm and impact scan

Load when scanning same-realm features or impact. Search the product
repo if one is in the workspace. If there is no repo, use only
surfaces the user provided and mark the rest unseen. Do not rely on
memory of a prior product.

## Where to look

Search in this order. Skip a source if it does not exist.

1. Product or app routes, nav, and settings screens
2. Feature flags, entitlements, and plan/tier gates
3. Domain models and APIs that already name the job
4. Admin, billing, notification, and email surfaces
5. Docs: README, AGENTS.md, product specs, help copy
6. Existing analytics event names (they often reveal shipped features)

Record the file or route you used. A feature you cannot point at is a
guess.

## Same-realm (overlap)

A feature is in the same realm when it:

- Does the same job for the same user
- Is a weaker or older version of the proposed job
- Is the place users already go to start this job
- Stores the object the new feature will create or edit

For each hit, say one of: **reuse**, **extend**, **replace**, or
**conflict**. Prefer reuse or extend over a second surface.

## Impact (blast radius)

A feature is impacted when the new work will change its:

- Entry point (nav, empty state, CTA, search)
- Data it reads or writes
- Permission, role, or entitlement check
- Notification, email, or in-product prompt
- Billing, quota, or usage display
- Shared component (table, modal, onboarding, settings row)

Mark **unseen** when you could not inspect a surface (no access, no
code, private admin). Do not silently drop it.

## Done when

- Overlap is a list, not "I think we already have something."
- Impact includes shared nav, data, and permissions, not only the new
  screen.
- Greenfield is claimed only after the scan found nothing in-realm.
