# W6 D5: ACL filtering, citations, abstention, cost + Friday design

Primer: `knowledge/06-rag.md` §5.

## The one idea

Three things separate an enterprise RAG demo from a system you can put in front of 10,000
employees:

1. **Access control inside retrieval.** Filter by the user's groups **before** taking the top-k.
   Post-filtering (top-k, then drop forbidden) returns fewer than k results for selective ACLs
   and tempts people to "fetch more and hope". Never filter in the LLM prompt.
2. **Citations you can check.** Every answer sentence cites chunk ids; a checker verifies each cited
   chunk actually supports the sentence. Today the support score is lexical: the fraction of the
   sentence's content words found in the cited chunks. Production uses an NLI model or an LLM
   judge; the structure is identical.
3. **Abstention.** If the best retrieval score is below a threshold, answer "I could not find this in
   the documents you can access" instead of guessing.

And a **cost model per query**: embedding + retrieval + LLM input + output tokens.

## Today's build (`w6d5_acl_citations.py`)

`acl_topk(scores, acl, user_groups, k)` (pre-filter), `support_score(sentence, chunk_texts)`,
`unsupported_sentences(answer, chunks, threshold)`, `should_abstain(top_scores, threshold)`,
`query_cost(...)`.

## Friday design (45 min)

`design.md`: an enterprise RAG platform for 10k employees. Timer, `my_design.md`, `rubric.md`,
model answer on `solutions`.

## Staff angle

The two questions that kill enterprise RAG projects late are "who can see what?" and "how do we
know it's right?". A staff engineer puts both in the first design review: the permission model
(mirrored from source systems, synced, enforced at retrieval, audited) and the eval plan (labelled
set, citation checks, online feedback, regression gate). Then the cost model, because finance asks next.
