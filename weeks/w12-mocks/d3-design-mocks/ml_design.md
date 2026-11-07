# Mock ML system design (45 min): LLM support-ticket triage

A B2B software company receives 50,000 support tickets per day in 6 languages. Today, a team of 60
agents reads every ticket, picks one of 140 categories and a priority, and routes it. Design an
LLM-based system that classifies, prioritises and routes tickets, drafts a first reply when possible,
and escalates to humans when unsure.

The interviewer will push on: label quality and taxonomy drift, how you evaluate (offline and online),
confidence and abstention, cost (where does it really come from?), latency, multilingual quality,
and the feedback loop from agents' corrections.
