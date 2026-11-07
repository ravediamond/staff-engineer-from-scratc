# Friday design #4: reward model and preference-data pipeline

**Timer: 45 minutes. Write in `my_design.md`.**

## Prompt

Your company is building a domain assistant for industrial maintenance engineers (think: your
own job). The team wants to move from prompt engineering to preference optimisation: collect
preference data, train a reward model, and use it for best-of-N at serving time and for DPO /
RL fine-tuning of an open-weight model. You have a budget of ~€150k for labelling in year one and
access to ~200 domain experts for a few hours a month.

Design the pipeline: data collection, labelling, RM training and evaluation, how the RM is used,
and how you keep it from being exploited.

## What the interviewer will push on

- Where do prompts and responses come from? How do you avoid labelling the easy stuff?
- Experts are scarce and expensive. How do you use them?
- How do you know the RM is good enough to optimise against?
- Reward hacking: what will the policy exploit and how will you notice?
- DPO vs online RL vs BoN: what would you do first and why?

## Deliverable

Requirements and non-goals · estimation (pairs, cost, compute) · data model · architecture ·
two deep dives · metrics, risks, scope.
