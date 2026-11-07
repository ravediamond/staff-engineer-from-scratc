# W5 D2: IDs, short codes, cursor pagination

Primer: `knowledge/05-design-method-and-estimation.md` §3.

## The one idea

**IDs.** Auto-increment in one database does not scale and leaks volume. UUIDv4 is random
(bad B-tree locality, 128 bits). **Snowflake-style IDs** (Twitter, Discord, and UUIDv7 in spirit)
pack time + worker + sequence into 64 bits, roughly time-ordered, generated locally with no
coordination:

```
| 1 bit 0 | 41 bits ms since custom epoch (~69 years) | 10 bits worker id | 12 bits sequence |
```
Same millisecond: increment sequence; sequence overflow (4,096/ms): wait for the next ms;
**clock moved backwards: refuse** (or you will generate duplicates).

**Short codes** (URL shortener): base62 of an integer ID. 7 chars = 62⁷ ≈ 3.5 × 10¹² codes.

**Pagination.** `OFFSET 10000 LIMIT 20` is slow (the DB walks 10,000 rows) and wrong under writes:
a new row inserted at the top shifts everything, so the next page repeats an item. **Cursor
(keyset) pagination**: the cursor encodes the last item's sort key, and the next page is "items
strictly after this key". The sort key must be **unique** (tie-break by id).

## Today's build (`w5d2_ids.py`)

`base62_encode/decode`, `Snowflake(worker_id, clock_ms).next_id()`, `snowflake_decode(id)`,
`encode_cursor/decode_cursor` (URL-safe base64 of JSON), and
`paginate(items, limit, cursor)` over items sorted by `(created_at desc, id desc)`.

## Staff angle

APIs outlive their implementations by a decade. A staff engineer pushes for opaque cursors
(clients cannot construct them, so the backend can change the sort or storage later), stable
idempotent writes (W2 D3), and versioning rules decided on day one. For ML-facing APIs: return
model version and request ids in every response, or you will never debug an eval regression
reported by a customer.
