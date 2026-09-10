# SQL Expert

Load during the SQL Expert step. Review every SQL query created,
edited, or newly called by the change. Optimize for the access
pattern named in the review, with a default bias toward **fast
reads**.

## Inventory

Search the change set and one hop of callers. Record location
(file + function or migration). A query you did not list was not
reviewed.

Look for:

- Raw SQL (`SELECT` / `INSERT` / `UPDATE` / `DELETE` / `WITH`)
- ORM and query builders (SQLAlchemy, Django, Prisma, Drizzle, Kysely, Peewee)
- Migrations, models, views, materialized views, generated columns
- Repository / DAO helpers the new code now calls

If the slice has no SQL after that search, mark N/A with the
patterns you used. Do not skip because "this is just an API change"
if the handler still hits the database.

## Access pattern

For each query, say how it is used — not how it looks.

| Pattern | Signals | Optimize for |
| --- | --- | --- |
| Read-heavy | List, detail, feed, search, dashboard, autocomplete; many reads per write | Read latency. Denormalize when joins or aggregations sit on the hot path. |
| Write-heavy | Ingest, webhooks, batch jobs, high-frequency updates | Write correctness and cheap writes. Do not denormalize first. |
| Mixed | Read and write both matter, or different shapes | Split: a write model plus a read model for the hot query. |

If the product use case is a user-facing API and you cannot prove
writes dominate, treat it as **read-heavy**.

## Read-speed refactor (default)

Work this list in order. Stop when the hot read is a single indexed
lookup or a purpose-built read row.

1. **Name the hot read.** Filters, sort, page size, columns returned,
   and the join graph today.
2. **Collapse the join.** If the request path joins several tables or
   aggregates on every read, propose a denormalized table, snapshot
   columns, or a materialized / maintained read model shaped like the
   response. Reads must not re-assemble the same graph each time.
3. **Index for what remains.** Match `WHERE`, `JOIN`, `ORDER BY`, and
   covering columns. Flag implicit scans, unmatched sorts, and
   leading-wildcard `LIKE`.
4. **Kill request-path waste.** N+1, lazy loads, `SELECT *`,
   unbounded result sets, filter-in-Python after fetch, per-row
   count queries, chatty existence checks.
5. **Keep writes honest.** Name how the denormalized copy stays
   current (same transaction write-through, DB trigger, or async
   rebuild) and what is allowed to lag.

A verdict of "add an index" is wrong when the hot path still walks
three tables for a list view. Prefer one fat read row over a
perfectly indexed join soup.

## Write-heavy and mixed

- Write-heavy: keep a normalized source of truth; batch writes;
  constrain and upsert; postpone denormalization unless a read
  path is already hurting.
- Mixed: do not make every consumer hit the write schema. Add a
  read model for the hot query; keep writes against the source
  tables.

## Verdicts

Use one per query:

- **keep** — already matches the access pattern
- **index** — shape is right; access path is not
- **rewrite** — same tables, better SQL/ORM (projection, pagination, no N+1)
- **schema-change** — denormalize, read model, generated column, or split

Each finding names the query, the access pattern, the hurt, and the
refactor. No generic "consider indexing" without a key and a query.

## Done when

- Every touched or newly called query has a verdict
- The hot path is explicit
- Read-heavy proposals make that read cheaper, including
  denormalization when joins dominate
- Write cost and consistency of any denormalized copy are named
