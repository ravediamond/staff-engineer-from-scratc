# Friday design #6: an agentic coding assistant and its evaluation

**Timer: 45 minutes. Write in `my_design.md`.**

## Prompt

Design an agentic coding assistant for a 2,000-engineer company: it takes a ticket, works in the
company's repositories (read code, edit, run tests and linters), and opens a pull request. Engineers
review the PRs. Leadership wants to know whether it is safe, whether it actually saves time, and what
it costs. You own the harness and the evaluation.

## What the interviewer will push on

- Execution environment and security: what can the agent touch, and what stops it?
- The loop: planning, tools, verification before claiming done ("prove it works").
- How do you evaluate it offline before rollout, and online after?
- How do you measure "saves time" honestly?
- Cost per PR and how you control it.
- Failure modes you expect in month one.

## Deliverable

Requirements and non-goals · estimation · architecture (harness, sandbox, tools, models) · two deep dives
(one must be evaluation) · metrics, risks, scope.
