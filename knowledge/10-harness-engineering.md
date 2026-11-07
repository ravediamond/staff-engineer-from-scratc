# 10. Harness engineering

## §1 The loop

Propose → validate against schema → execute (retries in the executor, idempotency for side effects) →
observation → repeat; budgets on steps, tokens, wall time, cost; explicit terminal statuses; loop detection.
Invalid args, unknown tools and tool failures are observations, not exceptions.

## §2 Sandboxing

Assume the model can be fully steered by prompt injection. Isolation (microVM/container per session),
no ambient credentials, egress allow-lists, path containment with realpath + commonpath, command policies
without a shell, timeouts, output caps, human approval for irreversible or external actions, audit logs.

## §3 Tracing, replay, verification

Span trees (OpenTelemetry GenAI conventions), recorded tool I/O, hermetic replay matched by tool and per-tool
call index with argument checks, trace diffs to find the first divergence, cost attribution.
Verification before "done": tests, checks, evidence attached (the "prove it works" principle).

## Lauren Tan's pstack, as a design pattern

pstack (a Cursor plugin, also loadable by Claude Code) packages a senior engineer's workflow as agent skills:
a router skill that picks a playbook per task type, research skills (how does the code work now, why is it this
way), design and competing-attempt skills, a multi-model review skill, verification skills that build and maintain
a CLI an agent can use to test the app, plus written principles ("Prove It Works", "Fix Root Causes"). The pattern
to copy: **principles as text, playbooks as procedures, verification as tools**, so agents and humans follow the
same rigorous loop. W10 D5 asks you to build your own.

## Questions

1. What makes an agent harness "trustworthy" at scale?
<details><summary>Answer</summary>Predictable behaviour under model failure (validation, errors as observations, budgets), safety under adversarial inputs (sandbox, least privilege, approvals), observability (every run traced and replayable), verification before claims, idempotent side effects, and an evaluation suite that gates every change to prompts, tools or models.</details>

2. MCP (Model Context Protocol): what is it and what does it change for harness design?
<details><summary>Answer</summary>An open protocol for exposing tools, resources and prompts to models through servers with a standard schema and transport. It decouples tool providers from harnesses (write once, use in many clients) but moves trust boundaries: third-party servers are untrusted code and content, so permissioning, sandboxing and auditing per server become harness responsibilities.</details>

3. How do you keep a coding agent from "passing" by editing the tests?
<details><summary>Answer</summary>Diff checks on test files (deleted tests, weakened assertions, added skips), hidden tests the agent cannot see (the eval holds them), requiring a failing-then-passing reproduction, protecting test directories by policy for certain task types, and reviewing test changes separately in the PR.</details>
