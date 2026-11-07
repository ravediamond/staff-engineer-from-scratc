# W10 D3: tracing, recording, deterministic replay

Primer: `knowledge/10-harness-engineering.md` §3.

## The one idea

You cannot debug, evaluate or regression-test an agent you cannot replay. Three pieces:

1. **Spans**: a tree of timed operations (`run → step → model call / tool call`) with attributes,
   status and output. OpenTelemetry's model; Arize Phoenix and LangSmith render exactly this.
2. **Recording**: every tool call's `(tool, args, output)` in order.
3. **Replay**: run the agent again, but tool calls return the **recorded** outputs instead of touching
   the world. Match each call by `(tool name, per-tool call index)` and **check the arguments** match:
   if the agent now calls the tool differently, that is a behaviour change, so raise a
   `ReplayMismatch` pointing at it, never silently return a recorded output for different args.

With replay, a prompt change can be tested against 500 recorded production traces in minutes, with
zero side effects, and a **trace diff** shows the first step where behaviour diverged.

## Today's build (`w10d3_tracing.py`)

`Tracer(clock)`: `start(name, parent=None, **attrs)`, `end(span_id, status, output=None)`, `children(span_id)`,
`duration(span_id)`. `Recorder(tools)` wraps tool functions and records calls. `Replayer(recording)` serves them
back with argument checks. `first_divergence(trace_a, trace_b)`, `run_cost(spans, usd_per_1k_in, usd_per_1k_out)`.

## Staff angle

Tracing is the substrate for evaluation, debugging, cost attribution and incident review, so a staff
engineer makes it non-optional in the harness (every run traced, sampled storage for high volume),
standardises the schema across teams (OpenTelemetry GenAI conventions), and makes "attach the trace id"
the first line of every bug report.
