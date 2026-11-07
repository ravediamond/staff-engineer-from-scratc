# Model answer: RM and preference pipeline (staff level)

## 1. Requirements
The RM drives: (a) best-of-N reranking at serving, (b) DPO training data selection and evaluation,
(c) filtering of synthetic training data. Quality bar: RM accuracy within 3 points of expert-expert
agreement on held-out prompts, calibrated (ECE < 0.05), no slice more than 5 points below average.
Non-goals: general chat quality, full online RLHF infrastructure in year one.

## 2. Estimation
Expert pair with rationale ≈ 3 min ≈ €4 at €80/h. €150k ≈ 35k expert pairs, or ~100k pairs if LLM
pre-labelling handles clear-cut pairs and experts adjudicate the 30% hardest. Plan: 10k expert pairs
in Q1 (pilot + RM v1), 25k by year end. RM: 7–8B model fine-tune with LoRA, hours on 8 GPUs. BoN-4 at
serving: 4× generation cost on the share of traffic it is enabled for.

## 3. Data model
Prompt (id, source, intent, language, sampled_at), Response (id, prompt id, generator model, params),
Comparison (prompt, response a, response b, label: a/b/tie/both-bad, annotator, rationale, time spent,
guideline version), Annotator (expertise, agreement score). Splits are assigned per prompt and stored.

## 4. Architecture
Traffic sampler (stratified by intent, rare intents oversampled) → response generators (current
prod model, candidate models, different temperatures, deliberately flawed variants) → active selection
(current RM ensemble disagreement or low margin) → labelling tool (expert queue for hard items, LLM
pre-label + spot-check for easy ones, 15% overlap, gold items) → QA (agreement, gold accuracy per
annotator) → dataset versions → RM training (ensemble of 3, prompt-level splits) → RM eval suite →
model registry → consumers: serving BoN, DPO trainer, data filter.

## 5. Deep dives
**Making experts count:** experts only see pairs where the RM ensemble disagrees or the LLM labeller
is unsure, plus 10% random for unbiased evaluation. Guidelines include domain-specific failure modes
(wrong torque value, unsafe step order). Rationales are collected briefly; they become rubric items
for an LLM judge later. Agreement is measured monthly; guideline updates are versioned.
**Avoiding exploitation:** BoN N chosen from a gold-vs-N curve measured by expert review on 300
prompts (expect a peak at N=4–8). DPO with β tuned on held-out expert preference win rate, not RM
score. Monitoring: answer length, citation rate, refusal rate, and the RM-vs-independent-judge gap on
production samples weekly; if the gap widens, refresh pairs on current policy outputs. Verifiable
checks (units, referenced procedure ids exist, numbers match the source document) as hard
constraints outside the RM.

## 6. Metrics, risks, scope
Metrics: RM accuracy vs agreement ceiling, ECE, expert win rate of BoN/DPO models vs baseline, length
drift, cost per labelled pair. Risks: expert fatigue (short sessions, gamification), narrow
annotator pool bias, RM learning style over correctness. Sequencing: BoN with RM v1 (no training risk,
measurable), then DPO on fresh pairs, online RL only if DPO plateaus and the reward is trustworthy.
