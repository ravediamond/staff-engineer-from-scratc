# Model answer: enterprise RAG platform (staff level)

## 1. Requirements
Users: technicians (procedures, troubleshooting), engineers (specs, standards), office staff (HR,
IT). Question types: lookup ("torque for flange X"), procedure ("how to replace seal on P-101"),
troubleshooting, policy. SLAs: p95 latency < 6 s to first token < 1.5 s; content freshness < 24 h
(< 1 h for safety documents); **permission changes enforced < 15 min**. Safety: answers about safety
procedures must quote the source verbatim with a link, or abstain. Non-goals v1: actions in other
systems (no agents writing tickets), drawings understanding beyond OCR text, external customers.

## 2. Estimation
10k users × 5 queries/day = 50k/day ≈ 0.6 QPS average, ~5 QPS peak: compute is small, cost is per token.
Per query: 3k input tokens (6 chunks × 400 + prompt), 300 output → at $3/$15 per M ≈ $0.0135 →
~$20k/month. Reranker on 50 candidates: small GPU or API, ~$2k/month. Corpus: 5M documents ×
~8 chunks = 40M chunks × 1024 dims ≈ 160 GB float32 (or 40 GB int8); embedding the corpus ≈ 40M
× 400 tokens = 1.6e10 tokens: one-off ~$1–3k. Dominant cost: LLM tokens.

## 3. API and data model
`POST /ask {question, conversation_id}` → stream {answer, citations[{chunk_id, doc_url, span}],
abstained, trace_id}. Chunk record: id = doc@version#i, text, embedding, doc metadata (source,
site, language, doc_type, safety_flag), ACL groups, version. Feedback: trace_id, rating, comment.

## 4. Architecture
Connectors (SharePoint Graph delta queries, Confluence webhooks, DMS crawl) → parse (layout-aware
PDF parser, table extraction, OCR for scans) → chunk (heading-aware, tables kept whole with headers)
→ embed (multilingual model) → index (hybrid: BM25 with per-language analyzers + vector, ACL and site
as filterable metadata) with version-checked upserts and tombstones. Query path: auth (SSO) → group
expansion (cached, 5 min TTL) → query understanding (language, safety intent) → hybrid retrieval with
ACL pre-filter → cross-encoder rerank top-50 → abstain check → context assembly → LLM with mandatory
citation format → citation checker (NLI) drops unsupported sentences → final ACL re-check → stream.

## 5. Deep dives
**Permissions:** ACLs mirrored per document as group ids; group membership from the identity provider
(SCIM), expanded at query time. Permission change events take a priority lane (metadata-only update,
no re-embedding) with a 15 min SLA, monitored. Before generation, the final chunk list is re-checked
against the source permission API for the user (defence in depth; 20–50 ms). Leak tests in CI: synthetic
documents with restricted ACLs and queries from unauthorised test users must never surface them.
Audit log of every chunk shown to every user.
**Evaluation and safety:** labelled set of 600 questions (9 languages, sliced by source and intent),
built from real queries and expert-written answers. Metrics: recall@10, answer correctness (LLM judge
calibrated against 2 experts, kappa > 0.7), citation support rate, abstention rate. Regression gate in
CI on every prompt/model/index change (paired bootstrap). Safety mode: if the question is classified as
safety-related, the answer is the verbatim procedure excerpt plus link, never a paraphrase; abstain if
retrieval confidence is low. Weekly review of thumbs-down answers by a domain owner.

## 6. Metrics, risks, scope
Online: answer rate, thumbs up/down, citation click-through, abstention, latency, cost/query, staleness,
permission-sync lag. Risks: scanned PDFs with poor OCR (measure per source), multilingual retrieval
gaps, users trusting wrong answers (UI shows sources prominently). Cost levers: route simple lookups
to a small model, cache frequent questions per ACL group, trim context with the reranker. Rollout:
one pilot site + one source, shadow mode against help-desk questions, then expand by source. Success
metric agreed upfront: e.g. 30% fewer expert escalations at the pilot site within 3 months.
