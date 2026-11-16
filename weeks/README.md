# The weeks, in order

One folder per week. **Open the week's `README.md` and follow it**: it holds the full lesson for the five days, the order of
work, and every command. Nothing outside the week folder is required to do the labs.

## Part 1: the core (12 weeks, 1 hour a day)

| Week | Open this | You end the week able to | Needs |
|---|---|---|---|
| 1 | [`w1-coding-base/README.md`](w1-coding-base/README.md) | build a heap, a hash map, an LRU cache, a trie and interval algorithms while narrating | Python |
| 2 | [`w2-reliability/README.md`](w2-reliability/README.md) | make calls safe: retries, circuit breakers, idempotency, rate limits, backpressure | week 1 |
| 3 | [`w3-distributed/README.md`](w3-distributed/README.md) | explain and build consistent hashing, quorums, vector clocks, Raft replication, fencing | weeks 1–2 |
| 4 | [`w4-storage-retrieval/README.md`](w4-storage-retrieval/README.md) | explain how a database stores data and how keyword and vector search work | weeks 1–3 |
| 5 | [`w5-design-method/README.md`](w5-design-method/README.md) | run a 45-minute system design with numbers; first timed design | weeks 1–4 |
| 6 | [`w6-rag/README.md`](w6-rag/README.md) | build and measure a RAG pipeline with access control and citations | week 4 |
| 7 | [`w7-evaluation/README.md`](w7-evaluation/README.md) | defend an evaluation: harness, judge calibration, statistics, A/B tests | week 6 |
| 8 | [`w8-reward-models/README.md`](w8-reward-models/README.md) | train and audit a reward model; explain over-optimisation and DPO | week 7 |
| 9 | [`w9-distributed-training/README.md`](w9-distributed-training/README.md) | answer "what breaks from 1 GPU to 64" from having built it | weeks 3, 8 |
| 10 | [`w10-harness-serving/README.md`](w10-harness-serving/README.md) | build an agent harness with sandbox and replay; size an LLM serving fleet | weeks 2, 5, 7 |
| 11 | [`w11-staff-judgment/README.md`](w11-staff-judgment/README.md) | root-cause, prove, write a design doc, migrate live, tell your stories | weeks 1–10 |
| 12 | [`w12-mocks/README.md`](w12-mocks/README.md) | pass coding, design, behavioral, deep-dive, take-home and pairing rounds | weeks 1–11 |

Weeks 5 to 10 end with a timed written design on Friday.

## Part 2: the blind sides (see `../ROADMAP.md`)

| Week | Open this | You end the week able to | Needs |
|---|---|---|---|
| 13 | [`w13-streaming/README.md`](w13-streaming/README.md) | explain Kafka from the log up, and design an event pipeline | weeks 2–4 |
| 14 | [`w14-kubernetes/README.md`](w14-kubernetes/README.md) | explain Kubernetes from the control loop up, and host and fine-tune LLMs on it | weeks 5, 9, 10 |
| 15 | [`w15-databases/README.md`](w15-databases/README.md) | reason about transactions, indexes, SQL, replicas and money | weeks 2–4 |

Weeks 13 and 14 each have a hands-on track on the real tools: `../handson/`.

## Inside a week folder

```
weeks/w1-coding-base/
  README.md                  the lesson for the whole week: read the day's section each day
  d1-heap/
    predict.md               1. guess, before reading
    README.md                   one-page summary of the lesson, with the staff angle
    predict_run.py           3. check your guesses
    w1d1_heap.py             4. the exercise: you write the code
    test_w1d1_heap.py           its tests
    review_w1d1.py           5. code with one planted bug: you fix it
    test_review_w1d1.py         its test
    questions.md             6. answer out loud
  d2-…/  d3-…/  d4-…/  d5-…/
```
Step 2 is reading the day's section of the week `README.md`. Friday folders of design weeks also hold `design.md` and `rubric.md`.
