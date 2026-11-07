# Questions

1. Walk through a zero-downtime migration of a vector index to a new embedding model.
2. Why must backfill respect versions? What happens without it?
3. What do you verify, and how do you set the mismatch threshold?
4. Tell me about a migration you led. What went wrong and what would you do differently? (your story)
5. How do you migrate the 30 internal clients of an API you are replacing?

## Model answers

1. New index built in parallel; the ingestion pipeline dual-writes new or updated docs to both, embedding with both models; a backfill re-embeds the corpus into the new index, checkpointed and rate-limited; verification compares coverage (every doc present at the right version) and quality (retrieval metrics on the labelled set, with a paired comparison); shadow reads compare results online; reads cut over behind a flag gradually (1%, 10%, 100%); old writes continue a week for rollback; then the old index is decommissioned.
2. Backfill reads a snapshot that can be older than concurrent dual writes; without a version check it overwrites newer data with stale data, a silent loss that verification may not catch if it compares against the same snapshot.
3. Coverage (missing keys), version currency, value equality (or semantic equality for derived data), and behavioural equivalence (sample queries returning equivalent results). Set the threshold before starting, based on the business tolerance; investigate every mismatch class before accepting a non-zero rate.
4. Your story. Shape: scope (systems, teams, data size), plan, the surprise (weird data, an unknown client), how you detected it (verification, canaries), the fix, the numbers (downtime 0, mismatches found and fixed), and what you would change.
5. Inventory clients (logs, not memory), publish a migration guide and a compatibility shim or adapter where possible, set a deprecation timeline with dates, give each client owner a dashboard of their remaining old-API traffic, offer migration help (office hours, PRs), escalate stragglers through their management with data, and turn the old API off only when traffic is zero or explicitly accepted.
