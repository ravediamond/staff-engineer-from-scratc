# Questions

1. Which retrieval metric matters most for RAG, and why?
2. Why is IDCG computed from all judgments? What happens otherwise?
3. 120 labelled queries. System B beats A by 0.03 recall@10. What do you need to say before claiming a win?
4. How do you build the labelled query set in the first place, cheaply and without bias?
5. Retrieval metrics improved; user satisfaction did not. Hypotheses?

## Model answers

1. Recall@k at the k you actually put in the context: if the evidence is not retrieved, the generator cannot use it. Then precision or nDCG, since noise and position in the context matter for long-context degradation and cost.
2. nDCG asks how close you are to the best possible ranking of all known relevant documents. With IDCG from the retrieved list, a system that retrieves one weak document ranks it "perfectly" and scores 1.0: the metric stops measuring what you missed.
3. A paired comparison (same queries) with a bootstrap CI or permutation test on per-query differences. If the CI includes 0, it is not a win. Also slice by query type (does it hurt one slice?) and check the latency or cost delta. With 120 queries, a 0.03 difference is often noise.
4. Sample real user queries from logs, stratified by intent and frequency; get relevance judged by domain experts on pooled results from several systems (pooling avoids bias toward the current system); use LLM-assisted pre-labelling with human verification on a calibrated subset; and keep a frozen held-out test set.
5. Answer quality is bound by generation (hallucination, poor synthesis, ignoring context), latency got worse, the query set does not represent real traffic, the UX (citations, formatting) is poor, or the wrong k was measured. Look at answer-level evals and per-slice metrics, and read 50 real failures.
