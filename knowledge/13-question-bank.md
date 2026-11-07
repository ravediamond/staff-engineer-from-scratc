# 13. Question bank (mixed, for warm-ups and mocks)

Pick five at random each mock day. Answer out loud in under two minutes each.

## Coding and fundamentals
1. Implement an LRU cache. Then make it thread-safe. Then distributed.
2. Find the k most frequent words in a 100 GB log file on one machine with 8 GB RAM.
3. Design and implement a rate limiter class with tests.
4. Merge overlapping time ranges from 1,000 services' maintenance windows.
5. Implement reservoir sampling and explain why it is uniform.

## System design
6. Design a URL shortener for 100M URLs/month.
7. Design a notification system (push, email, SMS) with user preferences and rate limits.
8. Design a distributed job scheduler for ML workloads.
9. Design a metrics/monitoring system (ingest 10M points/s, query dashboards).
10. Design a collaborative document editor.

## ML / AI systems
11. Design an enterprise RAG platform with permissions.
12. Design the evaluation platform for an AI product with 30 teams.
13. Design a recommendation system for a marketplace.
14. Design LLM serving for 10k QPS with a p95 latency SLO.
15. Design an agentic coding assistant and how you would evaluate it.
16. Design a reward model and preference-data pipeline.
17. Design a training platform for 512 GPUs.
18. Design fraud detection with real-time features and delayed labels.
19. Design content moderation with an LLM, a classifier cascade, and human review.
20. Design an A/B testing platform.

## Depth probes (follow-ups interviewers use)
21. Your eval says +2 points. How do you know it is real?
22. Your retrieval recall is 0.95 but answers are wrong. Where do you look?
23. Your DDP run diverges at 64 GPUs but not at 8. Why?
24. Your vector search p99 doubled after a data load. Why?
25. Your agent loops on the same tool call. What does the harness do?

## Behavioral and staff
26. Tell me about a time you set technical direction across teams.
27. Tell me about a decision you got wrong.
28. Tell me about a time you made a team faster without writing the code yourself.
29. Tell me about a conflict with a peer you respect.
30. What would you do in your first 90 days here?

## Pushback drills (the interviewer disagrees; hold or update, with reasons)
31. "Just use a bigger model, evaluation is overkill."
32. "We don't need idempotency, retries are rare."
33. "Fine-tuning will fix the hallucinations."
34. "Let's skip the design doc, we know what to build."
35. "Our offline eval improved, ship it."

<details><summary>How to answer a pushback drill</summary>

Acknowledge the strongest version of their point, state the risk with a number or an incident, propose the
cheapest experiment that would settle it, and say what result would change your mind. Example for 35: "Agreed
the offline gain is encouraging. Our offline-to-online agreement is about 70% over the last 20 launches, so
there's a real chance it doesn't transfer. A one-week A/B with latency and cost guardrails would settle it; if
the primary metric CI is above zero, we ship."
</details>
