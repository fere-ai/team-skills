# Zero states

Load when walking zero states. A zero state is any time the feature
is on screen (or should be) and the happy-path object is missing,
blocked, or failed.

Plan the empty case as a first-class screen, not a spinner or a blank
table.

## Surfaces to cover

For each new or changed surface, fill every row that applies:

| State | What the user sees | What they can do next |
| --- | --- | --- |
| Never used / first-run | | |
| Empty (account is valid, no objects yet) | | |
| Empty search / filter | | |
| Loading | | |
| Error / timeout / partial failure | | |
| Permission denied / wrong role | | |
| Entitlement or flag off | | |
| Integration not connected | | |
| After delete / reset | | |
| Existing data that does not fit the new model | | |

Skip a row only when that state cannot happen. Say so.

## Rules

- Empty is not an error. Tell the user what this space is for and the
  one action that fills it.
- First-run and empty-after-use can differ. Do not reuse onboarding
  copy on a cleared workspace.
- Denied and "not entitled" need a reason and an exit (ask admin,
  upgrade, wait for rollout). Do not look like a product bug.
- If the feature depends on another object (workspace, payment method,
  connected account), that missing object is a zero state of *this*
  feature.
- Existing users with legacy or partial data are a zero state, not an
  edge case for later.

## Done when

No new surface is described only with sample data in it.
