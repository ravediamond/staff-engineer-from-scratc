# W6 D4: freshness: versioned index, CDC, out-of-order events

Primer: `knowledge/06-rag.md` §4. Builds on W4 D5 (exactly-once consumer).

## The one idea

The index is a **derived view** of a source of truth (SharePoint, Confluence, a DB). It drifts:
documents change, get deleted, get permissions changed. Change-data-capture (CDC) streams
those events to the indexer. Events are **at-least-once** and can arrive **out of order**
(partitions, retries, backfills running alongside live updates).

**Invariant:** for each document, the index reflects the event with the **highest source
version** it has seen, and applying any event twice, or an older event late, changes nothing.

That means:
- store `version` per document; apply an event only if `event.version > stored.version`;
- deletes are **tombstones with a version** (not removal), otherwise a late older upsert resurrects a deleted doc;
- chunk ids derive from `(doc_id, version, i)` so old chunks can be removed atomically on update.

**Staleness** = documents whose indexed version < source version (or missing). It is a metric you alert on.

## Today's build (`w6d4_freshness.py`)

`VersionedIndex(chunk_size)`: `apply(event) -> bool`, `chunks_for(doc_id)`, `live_doc_ids()`,
`search(term)` (substring on live chunks: retrieval is not the point today), `staleness(source_versions) -> sorted doc ids`.

## Staff angle

Freshness is a product requirement with a price: "updates visible within 5 minutes" means
streaming CDC and incremental embedding; "within 24 hours" means a nightly batch. Ask what the
user needs, per source. And **permissions changes are freshness events too**: a doc whose ACL
was tightened must disappear from results within the security SLA, which is usually much
stricter than the content SLA (D5).
