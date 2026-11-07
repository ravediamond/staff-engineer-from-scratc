# W10 D1: the agent loop

Primer: `knowledge/10-harness-engineering.md` §1.

## The one idea

An agent is a loop: model proposes an action → harness validates → executes → feeds the
observation back → repeat until a final answer or a budget runs out. The model is the least
predictable component, so the harness must be the most predictable one:

- **Validate every tool call against its schema** before executing. Invalid args are not an
  exception: they are an **observation** sent back to the model ("arg `path` is required"), so it can fix itself.
- **Tool failures are observations too.** A crashed tool must not crash the run.
- **Unknown tool** → observation, not exception.
- **Budgets**: max steps and max tokens. When exhausted, stop with an explicit status
  (`"max_steps"`, `"budget"`), never loop forever.
- Every step goes into a **trace** (D3 replays it).

Today's schema language is a JSON-Schema subset: `type` (`object`, `string`, `integer`, `number`,
`boolean`, `array`), `properties`, `required`, `enum`, `items`, `additionalProperties: false`.

## Today's build (`w10d1_agent.py`)

`validate(schema, value, path="$")` → list of error strings, `Tool`, `run_agent(model, tools, task, max_steps, max_tokens)`
→ `{"status", "answer", "steps", "tokens", "trace"}`. A `ScriptedModel` is provided for tests.

## Staff angle

The staff decisions in a harness are about **where failure is handled and what is guaranteed**:
retries live in the tool executor (W2 D1), idempotency keys on side-effecting tools (W2 D3), budgets
per run and per user, a trace for every run, and a clear contract for what the model may and may not
do. Write those down as the harness's invariants; then every new tool is a reviewable diff against them.
