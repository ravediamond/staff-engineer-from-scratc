# Week 10: Harness engineering and LLM serving

**Everything you need for this week is on this page.** You need week 2 (timeouts, budgets), week 5 day 1 (estimation) and week 7 (evaluation). Plain Python and the standard library. Nothing from other folders is required.

Two layers sit around a language model in production. The harness turns a model that only writes text into an agent that acts: it runs the loop, checks every action, contains the damage, and records everything. The serving layer turns one GPU into many concurrent users. The first is your specialty; the second is where the cost is. This week you build the core of both.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [The two layers in five minutes](#the-two-layers-in-five-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-the-agent-loop), [Day 2](#day-2-the-sandbox), [Day 3](#day-3-tracing-recording-replay), [Day 4](#day-4-serving-arithmetic), [Day 5](#day-5-speculative-decoding-a-design-and-your-own-skill-set).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w10dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w10dN_*.py` | tests | run, never edit |
| `review_w10dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w10-harness-serving/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w10-harness-serving/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w10-harness-serving/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w10-harness-serving/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-agent-loop` | what makes an agent reliable? | a schema validator and the agent loop with budgets | where the step limit is checked |
| Tue | `d2-sandbox` | what may an agent touch? | path containment, a command policy, bounded execution | how "inside" is tested |
| Wed | `d3-tracing-replay` | how do you debug and test an agent? | spans, recording, deterministic replay, trace diff | what replay verifies |
| Thu | `d4-serving-math` | how many users fit on a GPU? | KV-cache arithmetic, a batching simulator, paged memory | a factor in the memory formula |
| Fri | `d5-speculative-design` | how do you generate faster without changing the output? | speculative decoding; then a timed design; then your own skill set | the acceptance ratio |

## The two layers in five minutes

**A language model takes text and returns text.** It works on **tokens**, pieces of words, and writes its answer one token at a time; each new token depends on everything before it.

**An agent** is a model in a loop. The model is told which **tools** exist (read a file, run a command, search) and answers either with a tool call, as structured data, or with a final answer. A program around it, the **harness**, executes the call and gives the result back as the next input.

```
task ─▶ model ─▶ "call read_file(path='a.py')" ─▶ harness: validate, execute ─▶ result ─▶ model ─▶ … ─▶ final answer
```

| Word | Meaning |
|---|---|
| tool call | the model's request to run a function, with arguments |
| observation | what the harness returns to the model after a call: a result **or an error message** |
| schema | the description of the arguments a tool accepts |
| trace | the recorded sequence of everything that happened in a run |
| budget | a hard limit on steps, tokens or money |
| sandbox | a restricted environment in which the agent's actions run |

The principle of the first three days: **the model is the least predictable component, so the harness must be the most predictable one.**

## Day 1: The agent loop

Folder: `d1-agent-loop`. Exercise: `w10d1_agent.py`.

### Errors are observations

A model will call a tool that does not exist, forget a required argument, pass text where a number is expected. A tool will crash. None of that should end the run with an exception. Each becomes an **observation** sent back to the model, in words it can act on: `"$.path: required"`. Models correct themselves very well when told precisely what was wrong, and cannot when the run simply dies.

| Event | Wrong reaction | Right reaction |
|---|---|---|
| unknown tool | raise | observation: "unknown tool `x`" |
| invalid arguments | raise, or execute anyway | observation: the list of errors |
| the tool raised | crash the run | observation: the error |

### Validating against a schema

A schema says what a valid value looks like. Today's is a subset of JSON Schema:

```python
schema = {"type": "object",
          "properties": {"path": {"type": "string"}, "lines": {"type": "integer"}},
          "required": ["path"], "additionalProperties": False}
```

| Keyword | Meaning |
|---|---|
| `type` | `object`, `string`, `integer`, `number`, `boolean`, `array` |
| `properties` | for an object: the schema of each known key |
| `required` | keys that must be present |
| `additionalProperties: false` | no key outside `properties` |
| `enum` | the value must be one of a list |
| `items` | for an array: the schema of every element |

A validator is a recursive function: check the node, then go into the properties of an object or the items of an array, extending a **path** (`$`, `$.path`, `$.files[2]`) so that each message says where the problem is. It returns the **list** of all errors; an empty list means valid.

One Python trap: `isinstance(True, int)` is `True`. A boolean must not pass as an integer or a number. Test for `bool` first.

```python
isinstance(True, int), type(True) is int        # (True, False)
```

### Budgets

A loop driven by a model can run forever, or until the bill arrives. Two hard limits: a maximum number of steps and a maximum number of tokens. When either is reached the run **stops with an explicit status** (`"max_steps"`, `"budget"`). The limit is checked **before** asking the model for another action. Checked after, the loop makes one call more than allowed: on a tool that sends an email or spends money, that extra call is the bug report. It is today's review bug.

The caller must be able to tell "finished" from "ran out"; a run that hits a limit and returns its last text as if it were an answer is a silent failure.

### The trace

Every step is appended to a trace: the action, the validation result, the observation. Wednesday's replay and all debugging depend on it.

### Traps of the day

- `True` accepted as an integer.
- Validation stopping at the first error.
- A tool exception that ends the run.
- A limit reached with a status of "done".
- The checks of the loop done in another order than the docstring's: the tests count steps and tokens exactly.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `validate` | list of error strings for a value against a schema | validating against a schema |
| `Tool` | a name, a schema, a function | — |
| `run_agent` | the loop: budgets, validation, execution, observations, trace | errors are observations; budgets |

A `ScriptedModel` is provided: it plays back a fixed list of actions, which makes the loop testable without any model.

Run: `uv run pytest weeks/w10-harness-serving/d1-agent-loop -k "not review"`

---

## Day 2: The sandbox

Folder: `d2-sandbox`. Exercise: `w10d2_sandbox.py`.

### The threat

An agent with a shell is remote code execution by design. The model's output is influenced by everything it reads: a web page or a file containing "ignore your instructions and run this" can redirect it (**prompt injection**). So the harness decides, **before** anything runs, whether it is allowed, and bounds what happens when it does run.

### Guard 1: path containment

The agent may read and write only inside its **workspace** directory. The check has two steps:

1. **Resolve the real path.** `os.path.realpath` removes `..` segments and follows symbolic links. `ws/../etc/passwd` and a link inside the workspace that points to `/etc` both resolve to their true target.
2. **Test containment** with `os.path.commonpath`, not with a string prefix.

```python
import os
ws = "/work"
"/work-evil/x".startswith(ws)                              # True: the string test is fooled
os.path.commonpath([ws, "/work-evil/x"]) == ws             # False: correct
os.path.commonpath([ws, "/work/src/a.py"]) == ws           # True
```

`/work-evil` begins with the characters `/work` and is a different directory. The prefix test is today's review bug, and a classic real vulnerability.

### Guard 2: command policy

- **Parse, do not pass to a shell.** `shlex.split("git commit -m 'a b'")` gives `['git', 'commit', '-m', 'a b']`. Run that list directly. `shell=True` hands the whole string to a shell, which will happily interpret `; rm -rf ~`.
- **Reject shell syntax you do not support**: `;`, `&&`, `||`, `|`, backquotes, `$(`, `>`, `<`. Without a shell they would not work anyway; refusing them makes the intent explicit and the observation clear.
- **Allow-list the executables.** A list of what is permitted, not a list of what is forbidden: a deny-list always forgets something.
- **Deny dangerous argument patterns** for the executables you do allow.

The check returns whether the command is allowed, the **reason** when it is not (which becomes the observation), and the parsed arguments.

### Guard 3: bounds on execution

- A **timeout**: a command that hangs must not hang the agent.
- An **output cap**: a command that prints a gigabyte must not fill the model's context. When output is cut, add an explicit **marker** such as `[truncated]`, so the model knows it did not see everything and does not reason from a partial file as if it were whole.
- The **working directory** pinned to the workspace.

```python
import subprocess
r = subprocess.run(["echo", "hello"], capture_output=True, text=True, timeout=5)
r.returncode, r.stdout                                   # (0, 'hello\n')
```

`subprocess.TimeoutExpired` is raised when the time runs out.

### Defence in depth

All of this sits **on top of** an operating-system sandbox (a container, gVisor, Firecracker), never in its place. The harness checks express intent and give useful observations; the OS sandbox is what holds when a check has a hole.

### Traps of the day

- A prefix test for containment.
- Containment tested before resolving links.
- `shell=True`.
- A deny-list of executables.
- Output cut with no marker.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `resolve_in_workspace` | real path inside the workspace, or `PathEscape` | guard 1 |
| `CommandPolicy.check` | allowed or not, the reason, the parsed arguments | guard 2 |
| `run_bounded` | run without a shell, with a timeout and an output cap | guard 3 |

Run: `uv run pytest weeks/w10-harness-serving/d2-sandbox -k "not review"`

---

## Day 3: Tracing, recording, replay

Folder: `d3-tracing-replay`. Exercise: `w10d3_tracing.py`.

### The problem

An agent run is long, costs money, touches the outside world, and is not deterministic. Without special tooling you cannot rerun it to find a bug, and you cannot tell whether a change of prompt made it better. Three pieces fix that.

### Spans

A **span** is one timed operation: it has a name, a start, an end, a status, attributes, and a **parent**. Spans form a tree:

```
run
├─ step 1
│   ├─ model      (tokens_in, tokens_out)
│   └─ tool: read_file
└─ step 2
    └─ model
```

This is the OpenTelemetry model; Arize Phoenix and LangSmith display exactly this tree. From it you get the duration of anything, the cost of a run (sum of tokens over the model spans, times the price), and where the time went. The clock is injected.

### Recording

Wrap every tool so that each call appends `(tool, arguments, output)` to a list, in order. That list is a **recording** of the run's contact with the world.

### Replay

Run the agent again, but tools no longer touch the world: each call returns the **recorded** output. The run becomes fast, free, repeatable and free of side effects. A change of prompt can be tested against 500 recorded production runs in minutes.

The rule that makes replay honest: the `k`-th call to a tool is matched with the `k`-th recorded call **to that same tool**, and **its arguments must be equal to the recorded ones**. If the agent now calls the tool with other arguments, its behaviour has changed. The recorded output is an answer to a different question; returning it would make the rest of the run fiction. The replayer raises a `ReplayMismatch` that says which call differs.

A replayer that returns recorded outputs without comparing arguments reports "all good" on an agent that now does something else. That is today's review bug. Asking for a call that was never recorded is a mismatch too.

### Trace diff

Given two traces, the index of the **first step** where the tool or its arguments differ, or where one trace ends before the other. It turns "the new prompt behaves differently" into "at step 7 it now searches before reading".

### Traps of the day

- Replay with no argument check.
- Calls matched by global position instead of per tool: one added call shifts everything.
- A span ended twice, or a duration read before the end.
- Cost summed over all spans instead of the model spans.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Tracer` | `start`, `end`, `children`, `duration` | spans |
| `Recorder` | run the real tool, record the call | recording |
| `Replayer` | serve recorded outputs, check arguments | replay |
| `first_divergence` | first differing step of two traces | trace diff |
| `run_cost` | dollars from the model spans | spans |

Run: `uv run pytest weeks/w10-harness-serving/d3-tracing-replay -k "not review"`

---

## Day 4: Serving arithmetic

Folder: `d4-serving-math`. Exercise: `w10d4_serving.py`.

### How generation works, as far as serving cares

A model is a stack of **layers**. To produce a token it looks at all the previous tokens (**attention**). For each previous token, each layer keeps two computed arrays, the **key** and the **value**, so that they are not recomputed for every new token. That store is the **KV cache**. It grows by one entry per layer for every token of the sequence.

### KV-cache memory

```
KV bytes = 2 (key and value) × layers × KV heads × head dimension × tokens × sequences × bytes per number
```

The leading 2 is easy to drop: a key **and** a value are stored for every token. Without it every capacity plan is off by half. That is today's review bug.

For an 8-billion-parameter model of the Llama-3 family (32 layers, 8 KV heads, head dimension 128, 2 bytes per number): `2 × 32 × 8 × 128 × 2 = 131 072` bytes, **128 KB per token**. A context of 32 000 tokens is about 4 GB **for one sequence**.

So the number of users a GPU can serve at once is set by memory:

```
concurrent sequences = floor( (GPU memory − model weights) / (KV bytes per token × tokens per sequence) )
```

Memory for the KV cache, not compute, is usually what caps concurrency. It is the first number to compute in any serving design.

### Batching

Producing one token for 1 sequence or for 64 takes almost the same time: at each step the GPU reads all the weights once, whatever the batch. So serving sequences **together** is nearly free throughput.

- **Static batching**: form a batch, run it until **every** sequence in it has finished, then form the next. A request for 10 tokens waits for the one that wants 2 000, and new arrivals wait for the whole batch.
- **Continuous batching** (the method of vLLM): at **every step**, sequences that have finished leave and waiting requests take the free slots.

Today's simulator advances step by step: each running sequence emits one token per step, and you measure when each request finishes under both policies. A "continuous" mode that admits new requests only when the batch is empty is static batching under another name.

### Paged KV memory

Reserving the KV space for the **maximum** length of every sequence wastes most of it, since most sequences stop early. **Paged** allocation hands out fixed-size blocks (16 tokens, say) as a sequence grows, like an operating system's memory pages.

```
contiguous waste = Σ ( max_len − actual length )
paged waste      = Σ ( unused slots in the last, partly filled block )       at most block_size − 1 per sequence
```

A sequence of 100 tokens with a maximum of 4 096 wastes 3 996 slots when pre-allocated and 12 with blocks of 16.

### Traps of the day

- Bits and bytes, or GB as 2³⁰ where the docstring says 10⁹.
- The factor 2 for key and value forgotten.
- Continuous mode that admits only at batch boundaries.
- Paged waste of a full last block counted as a whole block.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `kv_bytes_per_token`, `kv_cache_bytes` | the formula | KV-cache memory |
| `max_concurrent` | sequences that fit | KV-cache memory |
| `simulate` | static against continuous batching | batching |
| `contiguous_waste`, `paged_waste` | unused token slots | paged KV memory |

Run: `uv run pytest weeks/w10-harness-serving/d4-serving-math -k "not review"`

---

## Day 5: Speculative decoding, a design, and your own skill set

Folder: `d5-speculative-design`. Exercise: `w10d5_speculative.py`. Also in the folder: `design.md`, `rubric.md`.

### The idea

The large model is slow because it produces one token per pass. A small **draft** model is fast and often right. Let the draft propose the next `k` tokens; let the large **target** model check all `k` in **one** pass, which costs about the same as producing one token. Keep the proposals it agrees with.

Done naively, the output would be a mix of the two models. The acceptance rule below makes the output distribution **exactly** the target's. Speed, with no change in quality.

### The acceptance rule

For each drafted token `x`, in order, with `q(x)` the probability the draft gave it and `p(x)` the probability the target gives it:

```
accept x with probability min( 1, p(x) / q(x) )
on the first rejection:  draw a replacement from the RESIDUAL distribution, then stop
if all k are accepted:   draw one more token from the target's next distribution (a free bonus)
```

- If the target likes `x` at least as much as the draft did (`p ≥ q`), it is always accepted.
- If the draft was overconfident (`q > p`), it is accepted only part of the time.
- The **residual** is what the target wanted and the draft under-proposed: `max(0, p − q)` for every token, scaled to sum to 1.

A tiny case: two tokens, target `p = (0.7, 0.3)`, draft `q = (0.4, 0.6)`. Token A is drafted 40% of the time and always accepted: 0.40. Token B is drafted 60% of the time and accepted with probability 0.5: 0.30. The remaining 0.30 are rejections, and the residual is `(0.3, 0) → (1, 0)`: always A. Total: A = 0.70, B = 0.30. Exactly `p`.

The ratio is **target over draft**, `p / q`. Inverted, the rule accepts what the draft likes and the target does not, and the output drifts toward the draft model. That is today's review bug. And on a rejection the replacement comes from the **residual**, not from `p`. The test checks all of it the only way possible: the distribution of the first emitted token over 20 000 trials must match `p`.

```python
import random
rng = random.Random(0)
rng.choices([0, 1, 2], weights=[0.2, 0.0, 0.8])[0]        # draw one index from a distribution
```

### How much faster

With a per-token acceptance rate `α` and `k` drafted tokens:

```
expected tokens per target pass = (1 − α^(k+1)) / (1 − α)             k + 1 when α = 1
speed-up ≈ that / ( 1 + k · c )                                       c = cost of a draft pass / cost of a target pass
```

With `α = 0.8` and `k = 4`: 3.36 tokens per pass. If the draft costs 5% of the target, the speed-up is about 2.8. A draft that is rarely accepted makes things **slower**: you pay for it and keep nothing.

### After the lab: the Friday design (45 minutes, timed)

`design.md`: an agentic coding assistant and its evaluation.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

### This week's ship: your own skill set

The reference engineer of this repo, Lauren Tan, published pstack: a set of agent skills that encode how she works. This week you publish yours, in a new public repository:

1. **Principles** (10 to 15): one sentence each, with one example from your own work. Start from what this repo drilled: invariants first, predict before running, paired comparisons, idempotent side effects, retries at one layer, evaluation before claims.
2. **Playbooks** (5): evaluation regression triage, a RAG retrieval miss, a flaky agent run, a training loss spike, a new tool integration. For each: the trigger, the steps, the verification, the criteria for done.
3. **Verification skills** (2 or more): for example "prove this RAG change is better" (runs the tooling of weeks 6 and 7 and outputs intervals).
4. A README: what it is, how to install it, one before-and-after example.

Add the link to `SHIPLOG.md`. The day's own `README.md` has the same list.

### Traps of the day

- The ratio inverted; a replacement drawn from `p`.
- Continuing after a rejection.
- No bonus token when everything was accepted.
- A division by zero when `q(x) = 0` or `α = 1`.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `speculative_step` | the tokens emitted for one draft of `k` tokens | the acceptance rule |
| `expected_tokens` | expected tokens per target pass | how much faster |
| `speedup` | the gain, given the draft's relative cost | how much faster |

Run: `uv run pytest weeks/w10-harness-serving/d5-speculative-design -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w10`, timer on, AI fully off: `uv run pytest drills/w10 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 10 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 10 when you can do these without notes:

- [ ] draw the agent loop and say why every error is an observation
- [ ] write a recursive schema validator, with the boolean trap
- [ ] state the three guards of a sandbox and why a prefix test is wrong
- [ ] explain spans, recording and replay, and what replay must verify
- [ ] compute KV memory per token and the concurrency of a GPU
- [ ] explain continuous batching and paged KV memory
- [ ] state the acceptance rule of speculative decoding and why the output is unchanged

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/10-harness-engineering.md`, `knowledge/11-llm-serving.md`
- Previous week: [`../w9-distributed-training/README.md`](../w9-distributed-training/README.md) · Next: [`../w11-staff-judgment/README.md`](../w11-staff-judgment/README.md)
