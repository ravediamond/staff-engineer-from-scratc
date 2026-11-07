# Questions

1. Why must deletes be versioned tombstones?
2. How do you run a full backfill (e.g. new embedding model) while the live CDC stream keeps flowing?
3. Define and measure index staleness. What would you alert on?
4. A document's ACL is tightened. What is your SLA and mechanism?
5. Your source system has no CDC. Options?

## Model answers

1. Without a version on the delete, a late or duplicate upsert with an older version looks new and resurrects the document (possibly with content or permissions that should be gone). The tombstone remembers "deleted as of v3".
2. Both write through the same version-checked apply path, so order does not matter. The backfill reads a snapshot with source versions and the live stream applies newer ones. For a new embedding model, write into a new index; the live stream dual-writes to old and new; cut over after the backfill completes and quality checks pass.
3. The fraction or count of docs where indexed version < source version, plus age-weighted lag (time since the source changed). Measure by periodically sampling source versions or comparing CDC log position with consumer position. Alert on consumer lag above the SLA and on a stale fraction above a threshold, with separate, tighter thresholds for permission changes.
4. Security SLA (e.g. under 5 minutes, often stricter). Mechanism: ACLs stored as filterable metadata, separate from content, so a permission change updates metadata without re-embedding. Permission events get a high-priority path; at query time, re-check permissions against the source of truth (or a fresh ACL cache) for the final results before generation (defence in depth).
5. Periodic crawls with change detection (modified timestamps, ETags, content hashes), webhooks if the source supports them, or polling APIs with incremental cursors. Full re-crawl weekly to catch missed deletes (diff of ID sets). Document the resulting staleness SLA.
