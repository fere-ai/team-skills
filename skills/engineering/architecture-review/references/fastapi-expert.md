# FastAPI Expert

Load during the FastAPI Expert step. Review every controller
(path operation) created or edited in the change, plus dependencies
it uses. Goal: **async on the event loop, minimum work before the
response**.

## Inventory

Search for `FastAPI(`, `APIRouter`, `@app.get` / `post` / `put` /
`patch` / `delete` / `websocket`, and `@router.*`. List each route
with method, path, and handler name.

If the slice has no FastAPI after that search, mark N/A with the
patterns you used.

## Async is required

Every path operation and every dependency that does I/O must be
`async def`.

Flag immediately:

- `def` handlers (threadpool is not the house default)
- `async def` that then calls sync I/O (worse than a sync handler)
- Sync SQLAlchemy `Session`, `requests`, `httpx.Client`,
  `time.sleep`, blocking disk I/O, CPU-heavy work, or `.result()` /
  `.run_until_complete()` inside an async handler
- Sync ORM lazy-loads triggered while serializing the response

Replace with async session/client, `await asyncio.sleep`, thread offload
only for true CPU work, and explicit loads before the response.

## Request-path latency

The handler should do as little as possible, then return.

1. **One cheap read.** Align with the SQL Expert: if the route
   fans out to several queries, collapse to one read model rather
   than `asyncio.gather` as the end state. Gather is for truly
   independent I/O that must stay separate.
2. **No sequential awaits** of independent calls. If two network or
   DB calls do not depend on each other, run them concurrently —
   unless the SQL pass already replaced them with one query.
3. **Do not hold the request** for work the client does not need
   in this response (emails, analytics, cache warm, derived
   projections). Push those off the request path.
4. **Return only what the client needs.** Over-fetch plus Pydantic
   dump is still slow. Project in SQL; keep response models thin.
5. **Fail fast.** Timeouts on DB and HTTP clients, bounded queries,
   no unbounded `await` without a timeout story.
6. **Reuse connections.** Async engine / pool on the app, not a
   new engine per request. Startup and shutdown own the pool.

## Verdicts

Use one per route:

- **keep** — async, no blocking I/O, hot path is one cheap read
- **make-async** — signature or dependency is sync, or async wraps sync I/O
- **rewrite-for-latency** — async but the request path is still heavy
  (N queries, sequential I/O, work that belongs off-request)

Each finding names the route, the latency hurt, and the concrete
handler change. Tie SQL refactors here when the slowness is the
query shape, not the framework.

## Done when

- Every controller in the slice has a verdict
- Sync handlers and blocking calls are flagged or gone
- Independent I/O is concurrent, or better, collapsed with SQL
- Work not needed for the response is off the request path
