---
name: architecture-review
description: >-
  Reviews SQL and FastAPI for read speed and async latency. Use when
  doing an architecture review, reviewing SQL, FastAPI controllers,
  denormalization, read models, or optimizing API response times.
license: MIT
metadata:
  audience: engineering
  author: Pranav Prakash
  version: "0.1.0"
---

# Architecture review

Review a change set for query shape and request latency. Two required
lenses: SQL Expert (optimize for the real access pattern, especially
hot reads) and FastAPI Expert (every controller async and cheap on
the request path). Don't use for style-only PR review, incident
response, or a general ship checklist.

## When to use

Use on a diff, a PR, or a service slice that touches SQL, ORM
queries, schema, or FastAPI routes. Work from the repo in the
workspace. Produce the review in the conversation. Write a file
only if asked.

## Workflow

Copy this checklist and work through it in order:

```
Architecture Review Progress:
- [ ] Change set enumerated (SQL + FastAPI + call sites)
- [ ] Access pattern named (read-heavy / write-heavy / mixed)
- [ ] SQL Expert pass done (or N/A with search evidence)
- [ ] FastAPI Expert pass done (or N/A with search evidence)
- [ ] Refactors proposed against the hot path, not generic advice
- [ ] Trade-offs named (write cost, consistency, complexity)
```

1. **Enumerate the change set.** Use `git diff` / `git status` (or
   the files the user named). List every touched SQL string, ORM
   query, migration, model, and FastAPI path operation. Then search
   one hop out: callers of those queries and routers. Done when the
   list is files + symbols, not "the API layer."

2. **Name the access pattern.** From the product use case and the
   call sites, say which queries run most often and whether they
   are reads. Default bias: user-facing list, detail, feed, search,
   and dashboard paths are **read-heavy** — optimize those first.
   Write-heavy only when evidence says ingest, jobs, or admin
   writes dominate. Done when you can point at the hot path.

3. **SQL Expert.** Load
   [references/sql-expert.md](references/sql-expert.md). Review
   every query created or edited. If none, search the slice for
   SQL/ORM anyway; mark N/A only with what you searched. Propose a
   refactor sized for the access pattern (denormalize / read model
   when reads must be fast). Done when each query is keep, index,
   rewrite, or schema-change.

4. **FastAPI Expert.** Load
   [references/fastapi-expert.md](references/fastapi-expert.md).
   Review every controller in the slice. Require `async def` and a
   request path that does not block. Align with the SQL pass: do
   not `gather` five queries if one denormalized read would do.
   Mark N/A only with search evidence. Done when each route is
   keep, make-async, or rewrite-for-latency.

5. **Produce** the review below. **Verify** against the checklist.

## Output

```markdown
# Architecture review: [scope]

## Access pattern
- Dominant: read-heavy | write-heavy | mixed
- Hot path: [route or query + why it wins on volume]
- Evidence: [call site, product use, or "assumed read-heavy"]

## SQL Expert
### Queries reviewed
| Location | What it does | Pattern | Verdict |
### Findings
- [issue → why it hurts the hot path]
### Recommended refactor
- [concrete schema/query change]
- Trade-offs:
- If no SQL in slice: N/A — searched [paths/patterns]

## FastAPI Expert
### Controllers reviewed
| Route | Handler | Async? | Verdict |
### Findings
- [issue → why it adds latency]
### Recommended refactor
- [concrete handler/dependency change]
- If no FastAPI in slice: N/A — searched [paths/patterns]

## Cross-cuts
- [Where SQL shape and the controller should change together]
- Other structural notes (one line each, only if real):

## Open questions
- [Only what you could not verify]
```

## Pitfalls

- Reviewing SQL in isolation from how often it runs.
- Index-only advice when the hot read still joins on every request.
- Denormalizing a write-heavy path with no consistency plan.
- Calling a sync FastAPI handler "fine" because it works.
- Parallelizing N queries instead of collapsing them.
- Generic architecture essays — this skill ships a refactor.

## Verification

- [ ] Access pattern is named and tied to a hot path
- [ ] Every touched query has a verdict
- [ ] Every FastAPI controller has a verdict
- [ ] Read-heavy refactors aim at fast reads (including denormalize)
- [ ] FastAPI handlers are async or flagged
- [ ] Trade-offs are explicit
- [ ] N/A lenses include search evidence
- [ ] Output matches the template

## Resources

Load only the file the current step needs:

- [references/sql-expert.md](references/sql-expert.md) — query inventory, access pattern, read-speed refactors
- [references/fastapi-expert.md](references/fastapi-expert.md) — async controllers and request-path latency
