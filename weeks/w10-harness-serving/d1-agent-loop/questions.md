# Questions

1. Why are invalid tool arguments and tool failures observations rather than exceptions?
2. What budgets does a production agent need, and who sets them?
3. Where do retries live in an agent harness, and why only there?
4. How do you design tool schemas that models use correctly?
5. Your agent loops: it calls the same tool with the same args 30 times. How do you detect and handle it?

## Model answers

1. The model is a fallible caller that can repair its own mistakes if told what went wrong. Turning errors into observations keeps the run alive and gives the model a chance to correct (most models fix schema errors on the next turn), while the harness stays in control. Exceptions are for harness bugs, not model mistakes.
2. Max steps, max tokens (input and output), max wall time, max cost per run and per user per day, per-tool rate limits, and max side-effecting actions (e.g. at most 1 payment). Product sets them per plan; platform sets hard ceilings; the harness enforces them and reports which one stopped the run.
3. In the tool executor, for transient errors, with backoff and a retry budget (W2 D1). Not in the model loop (re-asking the model is expensive and changes behavior) and not in the tool itself if the executor already retries (amplification). Side-effecting tools retry only with idempotency keys.
4. Few tools with clear names, descriptions that state when to use them and when not, flat argument schemas with enums instead of free text, examples, consistent error messages, and outputs truncated and structured. Then measure tool-call accuracy and error rates per tool in evals, and iterate on the schema like an API.
5. Detect repetition in the trace (same tool + same canonical args N times, or an observation-hash cycle). Respond with an observation telling the model it is repeating and what it already got; if it continues, stop with status "loop_detected". Count it as an eval failure and add the case to the eval set.
