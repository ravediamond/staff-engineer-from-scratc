# Questions

1. Why pre-filter on ACL rather than post-filter, and what are the engine-level options?
2. How would you verify citations at scale?
3. How do you pick the abstention threshold?
4. Where does the money go in a RAG system, and the first three levers?
5. A user reports the assistant showed them a confidential HR document. Walk through your incident response and the design fixes.

## Model answers

1. Post-filtering returns fewer than k (often zero) results for selective permissions, and over-fetching to compensate is unbounded. Options: engine-native filtered ANN (Qdrant, Weaviate and OpenSearch apply filters during HNSW traversal), partitioning or a separate index per tenant/site for large groups, or exact search over the pre-filtered set when it is small.
2. An NLI model (entailment of the sentence by the cited chunk) or a small LLM judge per (sentence, cited chunk) pair, run on every answer in real time (drop or flag unsupported sentences) or on a sample offline. Calibrate the checker against human labels and track the support rate as a metric.
3. From data: on a labelled set, plot wrong-answer rate and abstention rate as the threshold varies; pick the point the product owner accepts (e.g. wrong answers under 3% at under 15% abstention), separately for safety-critical intents. Recalibrate when the retriever or model changes.
4. LLM tokens (input dominated by context), then reranking, then embeddings and storage. Levers: fewer and better chunks via the reranker (less input), routing easy queries to a smaller model, semantic caching per permission group, prompt caching of the static system prompt, and output limits.
5. Contain first (disable the source or the specific doc, invalidate caches), then preserve logs and identify scope from the audit log (who saw what, when). Root cause: ACL mirroring lag, group expansion error, missing ACL defaulting to public, or a cache shared across users. Fixes: missing ACL = nobody, a final re-check against the source at answer time, leak tests in CI, a permission-sync lag alert, and caches keyed by permission group. Postmortem with the security team.
