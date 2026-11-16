# Week 6: RAG (retrieval-augmented generation)

**Everything you need for this week is on this page.** You need week 4 (BM25, vector search, the exactly-once consumer). Nothing from other folders is required.

RAG is the most deployed LLM architecture, and one of your specialties. A demo takes an afternoon. A system that 10 000 employees can trust takes five things the demo skips: chunks that keep their source, retrieval that survives real queries, numbers that say whether it works, an index that follows the source documents, and access control and citations that hold. One day each.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [RAG in five minutes](#rag-in-five-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-chunking), [Day 2](#day-2-hybrid-retrieval-and-fusion), [Day 3](#day-3-retrieval-metrics-reranking-intervals), [Day 4](#day-4-freshness-versions-out-of-order-events), [Day 5](#day-5-access-control-citations-abstention-cost-then-a-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w6dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w6dN_*.py` | tests | run, never edit |
| `review_w6dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w6-rag/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w6-rag/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w6-rag/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w6-rag/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-chunking` | what can the retriever ever find? | three chunkers that keep source offsets | a gap in the coverage |
| Tue | `d2-hybrid-retrieval` | keywords or vectors? | both, fused | where ranks start |
| Wed | `d3-metrics-rerank` | does retrieval work, and how sure are you? | recall, MRR, nDCG, a reranker, bootstrap intervals | what "ideal" is computed from |
| Thu | `d4-freshness-cdc` | does the index follow the documents? | a versioned index fed by change events | what a late event may do |
| Fri | `d5-acl-citations` | may this user see it, and is the answer supported? | access-filtered retrieval, a citation checker, abstention, a cost model; then a timed design | when the filter is applied |

## RAG in five minutes

A language model knows what was in its training data. It does not know your company's documents, and when it does not know, it tends to invent. **Retrieval-augmented generation** gives it the relevant text at question time:

```
offline:   documents ──▶ split into chunks ──▶ index (keywords and/or vectors)
online:    question ──▶ retrieve the best chunks ──▶ prompt = instructions + chunks + question ──▶ model ──▶ answer with citations
```

| Word | Meaning |
|---|---|
| chunk | a passage of a document, the unit that is indexed and retrieved |
| retriever | the component that returns the top `k` chunks for a query |
| context | the retrieved chunks placed in the prompt |
| grounded | an answer whose statements are supported by the context |
| hallucination | a statement the context does not support |
| reranker | a slower, more accurate model that reorders the retriever's candidates |

The model can only use what retrieval gives it. **Most RAG failures are retrieval failures**: the right passage was never in the context. That is why four of the five days are about retrieval and its measurement.

## Day 1: Chunking

Folder: `d1-chunking`. Exercise: `w6d1_chunking.py`.

### Why chunking decides everything

Documents are too long to index or to put in a prompt whole, so they are cut into chunks. The cut sets a ceiling: a fact split across two chunks cannot be retrieved as a whole; a chunk that mixes three topics matches none of them well.

### Three strategies

**Fixed size with overlap.** Windows of `size` characters; each window starts `size − overlap` characters after the previous one. The overlap gives a sentence cut at a border a second chance to be whole in the next chunk. Simple, a fair baseline, and blind: it cuts in the middle of sentences and tables.

```python
text = "abcdefghij"; size, overlap = 4, 1
[(s, min(s + size, len(text))) for s in range(0, len(text), size - overlap)]
# [(0, 4), (3, 7), (6, 10), (9, 10)]: the last one lies inside the one before and should not be kept
```

**Recursive.** Try to cut at the strongest natural boundary first. Given separators from strongest to weakest (blank line, newline, end of sentence, space): if the text fits in `max_len`, it is one chunk. Otherwise split on the first separator that occurs in it, apply the same procedure to pieces that are still too long with the weaker separators, then merge neighbouring small pieces back together while they fit. A piece with no separator left stays whole even if too long.

**Heading-aware.** For structured documents, cut at headings. Each chunk remembers its **heading path**, such as `Install > Linux > Troubleshooting`. The path is metadata: it can be added to the chunk's text before embedding, and shown in the citation.

```python
"## Linux setup".startswith("## "), len("###") <= 6       # a Markdown heading: 1 to 6 '#', then a space
```

| Strategy | Good for | Weak at |
|---|---|---|
| fixed + overlap | baselines, uniform text | sentences, tables |
| recursive | prose | document structure |
| heading-aware | manuals, wikis | very long sections (they need a second pass) |

### The invariant: offsets, and no gaps

Every chunk keeps `(start, end)`: where it sits in the source text. And the chunks **cover the source with no gap**: every character belongs to at least one chunk.

Offsets are what a citation points to, and how you debug "why did we not retrieve this?": find the passage, find its chunk. A splitter that drops the separators, or strips whitespace and loses count, produces chunks whose offsets are wrong or that skip characters. Check it directly: `text[start:end]` must be the chunk's text.

### Traps of the day

- A last chunk entirely inside the previous one.
- Separators dropped: gaps in the coverage.
- An overlap as large as the size: the window never advances.
- Offsets computed on a modified copy of the text.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `fixed_spans` | windows with overlap | fixed size with overlap |
| `recursive_spans` | split on the strongest separator, merge up to `max_len` | recursive |
| `heading_chunks` | one chunk per heading, with its path | heading-aware |
| `to_records` | spans → records with id, offsets and text | the invariant |

Run: `uv run pytest weeks/w6-rag/d1-chunking -k "not review"`

---

## Day 2: Hybrid retrieval and fusion

Folder: `d2-hybrid-retrieval`. Exercise: `w6d2_hybrid.py`.

### Two retrievers that fail on different queries

| | Lexical (BM25, week 4 day 3) | Dense (vectors, week 4 day 4) |
|---|---|---|
| Matches | the same words | similar meaning |
| Fails on | paraphrases: "car" against "automobile" | identifiers, error codes, rare names: `ERR_4012` |

Since they fail on different queries, combining them almost always beats either one. That is **hybrid retrieval**, and it is the default in production.

### Reciprocal rank fusion (RRF)

The two retrievers produce scores on unrelated scales, so adding scores makes no sense. RRF ignores the scores and uses only the **rank** of each document in each list:

```
RRF(d) = Σ over the lists that contain d of   1 / (k + rank of d in that list)        rank starts at 1; k = 60 by convention
```

A document ranked first in both lists gets `2/61`; one ranked first in one list only gets `1/61`. The constant `k` flattens the difference between neighbouring ranks, so that no single list dominates. A document absent from a list contributes nothing for it.

Ranks start at **1**. With ranks from 0, the first document's term is `1/60` instead of `1/61`: the order of close results changes, and the results no longer match anyone else's implementation. That is today's review bug.

### Score fusion

The alternative: bring each list's scores to a common scale, then take a weighted sum. **Min-max** maps a list's scores to [0, 1]: `(s − min) / (max − min)`. When all scores are equal the denominator is zero; the docstring says what to return. It is tunable through the weights, and fragile: one outlier score squeezes all the others toward 0.

### Today's dense side: the hashing trick

A real embedding model would be a large download. Today's vector is built by **feature hashing**: each word and each pair of neighbouring words (bigram) is hashed to a position in a vector of size `dim`, and adds `+1` or `−1` there (the sign also comes from the hash, so that collisions tend to cancel). The vector is then scaled to length 1. It is deterministic and needs no model. It captures shared words and word pairs, not meaning; it is enough to make fusion visible. In production you replace it with a real encoder and nothing else changes.

### Traps of the day

- Ranks from 0.
- Raw scores of the two retrievers added.
- Ties left in arbitrary order: break them by document id.
- The dense vectors not normalised (week 4).

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `hash_embed` | hashed unigrams and bigrams, signed, normalised | the hashing trick |
| `rrf` | fuse ranked lists | reciprocal rank fusion |
| `minmax_fuse` | normalise and weight score dicts | score fusion |
| `HybridIndex.search` | modes `bm25`, `dense`, `rrf` | two retrievers |

Run: `uv run pytest weeks/w6-rag/d2-hybrid-retrieval -k "not review"`

---

## Day 3: Retrieval metrics, reranking, intervals

Folder: `d3-metrics-rerank`. Exercise: `w6d3_metrics.py`.

### What you need to measure anything

A set of queries, and for each query the documents that are relevant: the **relevance judgments**, or **qrels**. They may be graded (0 not relevant, 1 to 3 increasingly relevant). The system's output for a query is a ranked list.

### Four metrics

| Metric | Per query | It answers |
|---|---|---|
| recall@k | relevant documents in the top `k` / all relevant documents | did we retrieve the evidence at all? **The one RAG needs most.** |
| precision@k | relevant documents in the top `k` / `k` | how much noise enters the context? |
| MRR | 1 / rank of the first relevant document (0 if none) | how high is the first good hit? |
| nDCG@k | see below | graded relevance, with position |

**nDCG.** Each result at position `i` (from 1) contributes a **gain** that grows with its grade, divided by a **discount** that grows with its position:

```
DCG@k  = Σ_{i=1..k}  (2^grade_i − 1) / log2(i + 1)
nDCG@k = DCG@k / IDCG@k
```

**IDCG** is the DCG of the **ideal** ranking: all the judged documents of the query, sorted by grade, best first. Dividing by it puts the score between 0 and 1.

The ideal ranking is built from **all the qrels**, not from the documents the system happened to return. Built from the returned list, the "ideal" is just that list re-sorted, and every system scores close to 1, including one that missed the best document entirely. That is today's review bug.

A worked value: grades of the returned list `[3, 0, 2]`, and the qrels contain grades 3, 2, 1. DCG = `7/1 + 0/1.585 + 3/2 = 8.5`. Ideal order `[3, 2, 1]`: IDCG = `7/1 + 3/1.585 + 1/2 = 9.39`. nDCG = 0.905.

### How sure are you: the bootstrap

A mean over 100 queries is an estimate. Change the queries and it moves. The **bootstrap** measures by how much: draw 100 queries from your 100 **with replacement**, recompute the mean, repeat a thousand times. The 2.5th and 97.5th percentiles of those means are a 95% **confidence interval**.

```python
import random
rng = random.Random(0)
scores = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
means = sorted(sum(rng.choices(scores, k=len(scores))) / len(scores) for _ in range(1000))
means[25], means[974]                       # a 95% interval for a mean of 0.7: wide, with only 10 queries
```

Report every retrieval number with its interval. "Recall@10 went from 0.71 to 0.74" on 100 queries is usually inside the noise.

### Reranking

A **two-stage** design: a cheap retriever returns a generous list (say 100 candidates); an expensive, accurate scorer looks at each candidate together with the query and reorders them; the top `k` go to the model. The first stage must have good **recall** (a document it missed cannot be recovered); the second stage provides the **precision**. Today the scorer is a function you pass in. A **stable** sort keeps the original order among equal scores; Python's `sorted` is stable.

### Traps of the day

- IDCG from the retrieved list.
- Recall divided by `k`.
- A query with no relevant document crashing instead of scoring 0.
- The discount `log2(i + 1)` with `i` from 0: a division by zero.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `recall_at_k`, `precision_at_k`, `reciprocal_rank` | the first three metrics | four metrics |
| `ndcg_at_k` | graded, with IDCG from all qrels | nDCG |
| `rerank` | rescore candidates, keep the top `k`, stable | reranking |
| `bootstrap_ci` | mean and interval | the bootstrap |
| `evaluate` | each metric with its interval over all queries | all of the above |

Run: `uv run pytest weeks/w6-rag/d3-metrics-rerank -k "not review"`

---

## Day 4: Freshness, versions, out-of-order events

Folder: `d4-freshness-cdc`. Exercise: `w6d4_freshness.py`.

### The index is a copy, and copies drift

The index is a **derived view** of a source of truth: a document system, a wiki, a database. Documents change, are deleted, change permissions. An index that does not follow serves old answers and, worse, deleted or forbidden content.

**Change data capture (CDC)** is the stream of change events from the source: "document 12 is now at version 5, here is its text", "document 12 was deleted at version 6". The indexer consumes it.

Two facts about that stream, from weeks 2 and 4: events are delivered **at least once**, so duplicates happen; and they can arrive **out of order**, for instance when a bulk re-import runs next to live updates.

### The invariant

For each document, the index reflects the event with the **highest version** it has seen. Applying an event twice, or applying an older event late, changes nothing.

Three rules produce it:

1. **Store the version per document, and apply an event only if its version is higher than the stored one.** Duplicates and late events are then ignored by themselves.
2. **A delete is a tombstone with a version,** not a removal. If a delete at version 6 erased every trace of the document, a late "version 5" event would find nothing stored, look new, and bring the deleted document back.
3. **Chunk ids derive from `(doc_id, version, index)`.** When a document is updated, all chunks of its old version are removed and the new ones added in one step. Chunks of two versions never mix.

```
event order received:   upsert v5   delete v6   upsert v4 (late)   delete v6 (duplicate)
stored version:           5            6 (tombstone)   6 (ignored)        6 (ignored)
```

### Staleness is a metric

A document is **stale** when its indexed version is lower than its version at the source, or when it is missing from the index. The list of stale documents is something you compute, graph, and alert on: "0.3% of documents are more than one hour behind". A RAG system without that number does not know whether its answers are current.

### Traps of the day

- A late older event applied.
- A delete that forgets the version.
- A deleted document still returned by search: tombstoned documents are not live.
- Old chunks left behind after an update.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `VersionedIndex.apply` | apply an event if it is newer; return whether it was applied | the invariant |
| `chunks_for`, `live_doc_ids`, `search` | what the index currently serves | the invariant |
| `staleness` | documents behind their source version | staleness is a metric |

Run: `uv run pytest weeks/w6-rag/d4-freshness-cdc -k "not review"`

---

## Day 5: Access control, citations, abstention, cost; then a design

Folder: `d5-acl-citations`. Exercise: `w6d5_acl_citations.py`. Also in the folder: `design.md`, `rubric.md`.

### Access control inside retrieval

In a company, each document is visible to some groups. A user must never receive a passage from a document they cannot open, not even paraphrased by the model.

- **Pre-filter**: keep only the chunks the user may see, **then** take the top `k`.
- **Post-filter**: take the top `k`, then drop the forbidden ones. A user with narrow access may be left with 1 result out of 10, or none, while good permitted chunks sat at rank 11 and beyond.
- **Filtering in the prompt** ("do not reveal confidential content") is not access control. The text is already in the model's context and can leak.

A chunk with no access list is visible to **nobody**. When in doubt, deny.

```python
{"eng", "all"} & {"hr"}, bool({"eng", "all"} & {"all", "sales"})       # (set(), True): no shared group; one shared group
```

### Citations you can check

Each sentence of the answer cites the chunks it relies on. A **checker** verifies that the cited chunks really support the sentence. A sentence is unsupported if it cites nothing, cites a chunk that does not exist, or is not backed by what it cites.

Today "backed" is measured lexically: the fraction of the sentence's **content words** (words that carry meaning, without "the", "of", "is"…) found in the cited chunks. Production systems use an entailment model or an LLM judge in that place. The structure around it is the same: sentence, citations, support score, threshold.

### Abstention

If the best retrieval score is below a threshold, or nothing was retrieved, the right answer is "I could not find this in the documents you can access". A wrong answer delivered with confidence costs far more trust than an honest "not found". The threshold is tuned on a set of questions that have no answer in the corpus.

### A cost model per query

Embedding the query + the retrieval + the model's input tokens (instructions, the chunks, the question) + its output tokens. Input tokens usually dominate, and they scale with `k × chunk size`: retrieving twice as many chunks roughly doubles the cost of every query. Have the number per query and per month before the design review asks.

### After the lab: the Friday design (45 minutes, timed)

`design.md`: an enterprise RAG platform for 10 000 employees.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

Every day of this week is a deep dive you can choose: chunking, hybrid retrieval, evaluation with intervals, freshness, access control.

### Traps of the day

- Top `k` taken before the access filter.
- A missing access list treated as "public".
- A sentence with no citation counted as supported.
- No abstention when nothing was retrieved.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `acl_topk` | filter by group, then top `k` | access control |
| `support_score`, `unsupported_sentences` | the citation checker | citations |
| `should_abstain` | no results, or best score under the threshold | abstention |
| `query_cost` | dollars for one query | a cost model |

Run: `uv run pytest weeks/w6-rag/d5-acl-citations -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w06`, timer on, AI fully off: `uv run pytest drills/w06 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 6 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 6 when you can do these without notes:

- [ ] draw the offline and online paths of a RAG system
- [ ] compare three chunking strategies and state the offsets-and-coverage invariant
- [ ] say when BM25 fails and when dense retrieval fails, and write RRF
- [ ] define recall@k, MRR and nDCG, and say what IDCG is computed from
- [ ] explain a bootstrap interval and why a retrieval number needs one
- [ ] state the three rules that make an index safe under duplicate and late events
- [ ] explain pre-filter against post-filter, the citation checker and abstention

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/06-rag.md`
- Previous week: [`../w5-design-method/README.md`](../w5-design-method/README.md) · Next: [`../w7-evaluation/README.md`](../w7-evaluation/README.md)
