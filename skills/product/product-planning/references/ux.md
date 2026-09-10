# UX: consistency, copy, one-pass flow, loaders

Load this file when checking the feature's words and path. This is not
a visual design pass, a brand pass, or an accessibility spec.

Read existing screens, nav, empty states, and buttons in the repo
before proposing new ones.

## Consistency with what already shipped

A new surface must look like it belongs to this product.

- Reuse the existing pattern for the same job (list + create, settings
  row, modal confirm, empty state). Invent a new pattern only when
  none fits — say why.
- Reuse the words the product already uses for the same object and
  action. Do not mint a synonym ("Workspace" next to "Project" for
  the same thing).
- Put the feature where a current user would look first (same nav
  family, same settings cluster, same object page). A second home
  is an inconsistency.
- Match affordances: primary vs secondary actions, destructive
  confirmations, where help and errors appear.

Flag every place the new flow would teach a different habit than the
rest of the product.

## Copy: one read, human, precise

Write for a regular internet user. They should read the label,
instruction, or error **once** and know what to do. If they need to
read it twice, rewrite it.

- Everyday words. No internal jargon, no marketing tone, no clever
  phrasing.
- Precise verbs that match what the product actually does. If the
  platform only does text chats, do not say "talk." If nothing is
  sent until they click, do not say it is "live." Name the real
  object and the real action.
- Prefer a concrete outcome over a vague label ("Save changes", not
  "Apply"; "Delete report", not "Remove").
- Errors say what happened and what to do next. Do not blame the
  user. Do not claim success before it happened.
- Empty and first-use copy follows the same one-read rules.

Scan existing UI strings in the repo and match that vocabulary unless
the old word is wrong — then change it everywhere this feature
touches, do not fork the language.

## One-pass flow

An average internet user should understand the workflow in one go.
No tutorial, no second reading of the screen, no remembering a rule
from two steps ago.

- One job per path. Extra decisions belong later or out of bounds.
- The next action is visible on the screen that needs it.
- Do not make the user remember an id, a setting, or a warning from
  a previous step — keep that context on screen.
- Irreversible actions are obvious before they happen.
- If two options exist, the difference is a consequence they care
  about, not a synonym.

Walk the happy path out loud in plain language. If you cannot explain
it in one short breath, the flow is not ready.

## Loaders and API failures

Many surfaces ship with no wait state. A new feature must show that a
call is in progress, and recover when it fails.

- Every fetch, save, delete, or other API wait has a visible loader
  (page, section, list, or button). A frozen or blank screen while a
  call is in flight is a gap.
- Reuse the product's existing loader if one exists. Do not invent a
  second spinner style.
- The control that started the call looks busy (loader on the button
  or the region it fills). Do not leave it clickable as if nothing
  happened.
- Failures are graceful: say what happened in one read, keep the
  user's input, offer a next step (try again, go back). Do not show
  a raw error, a blank page, or a success that did not happen.
- Timeouts and partial results are failures too. Name what loaded
  and what did not.

## Done when

- New UI reuses existing patterns and words, or each break is named
- Every new string passes a one-read test
- Verbs match what the product does
- The core job is completable without rereading or a guide
- Every new API wait has a named loader
- Every new API failure has copy and a next step
