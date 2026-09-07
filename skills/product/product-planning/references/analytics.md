# Analytics inventory

Load when inventorying analytics. The job is coverage of the
feature's journeys on platforms this product already uses — not a
generic tracking wishlist. Search the repo if one is in the
workspace. If there is no repo, use only integrations the user
named and mark the rest unseen.

## 1. Discover platforms

Search the repo for SDK init, env examples, and package names. Common
signals:

- Customer.io — `customerio`, `cioanalytics`, `cio-`
- PostHog — `posthog`, `phc_` in examples only (never commit secrets)
- Google Analytics — `gtag`, `G-`, `GA4`, `google-analytics`
- Datadog — `datadog`, `DD_`, RUM, `browser-logs`
- Others: Segment, Mixpanel, Amplitude, Sentry, LogRocket

List only platforms you found. If none are found, say so and plan
instrumentation against whatever the team already standardizes on —
do not invent a stack.

## 2. Map journeys to events

From the locked intention, list the actions that prove the feature
works:

- Viewed / entered the feature (including a zero state)
- Completed the core job
- Failed or abandoned the core job
- Changed a setting that alters the job
- Existing user first use vs new user first use, if those paths differ

Reuse existing event names and properties when they already mean the
same thing. Do not mint a parallel taxonomy.

For each action:

| Action | Event name | Properties | Identity | Platforms | Status |
| --- | --- | --- | --- | --- | --- |
| | | | user/account/anon | | exists / planned / gap |

Status **exists** only if you saw it in code or in a live catalog.
**Planned** is a named event the spec will add. **Gap** is a journey
with no event.

## 3. Live check (only if a tool is available)

After the code (or repo) scan, if a tool can query a connected
platform, verify definitions there. Otherwise skip and mark the live
check unseen. No specific agent or IDE is required.

- PostHog: confirm the event exists and which properties are on it
- Customer.io: confirm the event or attribute can be used in a
  campaign or segment
- Datadog: confirm the RUM/action or metric name you would alert on
- Any other platform: same bar if a query tool exists; otherwise
  rely on the repo and mark live verification unseen

Never paste live API keys, tokens, or project secrets into the brief.

## 4. Bar for "analytics are available"

The feature is covered when:

- Each key journey has an exists or planned event
- The same event is not planned under two names
- Identity matches how this product already identifies users
- Zero-state views are visible if empty is a meaningful product state
- Failures are visible, not only successes

If a platform is integrated but this feature will not send to it, say
why (example: Datadog is infra-only; product events live in PostHog).

## Done when

The brief's Analytics section lists platforms found, the journey map,
and gaps. Unverified live catalogs sit under Open questions.
