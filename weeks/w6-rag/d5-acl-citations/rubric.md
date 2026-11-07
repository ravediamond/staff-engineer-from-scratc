# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | features listed | users and question types characterised, latency and freshness SLAs per source, safety requirement made explicit, non-goals |
| 2 | Estimation | some numbers | queries/day, tokens/query, $/query and $/month, corpus size → chunks → embedding cost and storage |
| 3 | Ingestion | "connectors" | per-source connectors, parsing per document family (tables, scans/OCR), versioned upserts, CDC or crawl, staleness metric |
| 4 | Retrieval | "vector DB" | hybrid + reranker, multilingual handling, ACL as metadata pre-filter, top-k chosen by eval |
| 5 | Permissions | "check permissions" | ACL mirroring, group expansion, security SLA for changes, re-check at answer time, audit log, leak tests in CI |
| 6 | Generation | "prompt the LLM" | context assembly, mandatory citations, citation checker, abstention threshold, safety-procedure mode (quote verbatim, link to source) |
| 7 | Evaluation | "user feedback" | labelled set per language/slice, retrieval and answer metrics, LLM-judge calibrated vs humans, regression gate, online feedback loop |
| 8 | Cost | none | cost model with dominant term identified; levers (caching, smaller model routing, context trimming) |
| 9 | Operations | none | observability per stage, trace ids, incident playbook for a wrong safety answer |
| 10 | Scope and rollout | none | pilot site, shadow mode, what not to build in v1, success metric agreed with the business |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
