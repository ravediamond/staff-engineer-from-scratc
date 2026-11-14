# W13 D4: stream processing: event time, watermarks, checkpoints

Primer: `knowledge/16-streaming-and-messaging.md` §4. Book: *Streaming Systems* (Akidau), ch. 2–3.

## The one idea

Every event has two times: **event time** (when it happened, a field in the record) and **processing
time** (when your job sees it). Networks, retries and offline phones make events arrive **out of
order**. "Clicks per minute" must mean per minute of event time, or the result changes with every replay.

To close a window you must decide that no more events for it will arrive. A **watermark** is that
claim: "I have seen everything up to time W". The usual heuristic, per input partition:
`max event time seen − max_out_of_order`. With several partitions the job's watermark is the
**minimum** over them: one slow partition holds everyone back (and an idle one stalls the job: real
engines have idle-source timeouts).

- A window `[start, start + size)` **fires** when `watermark ≥ end`.
- **Allowed lateness**: keep the window's state until `watermark ≥ end + lateness`; a late event inside
  that period updates the result and the window fires again (an **update**).
- After that, late events go to a **side output** (dead-letter): never dropped silently.

**Fault tolerance.** A checkpoint stores the operator state **together with** the input offsets it
reflects. After a crash: restore state, rewind inputs to those offsets, replay. State is then
exactly-once. Outputs are exactly-once only if the sink is idempotent or transactional (two-phase
commit tied to the checkpoint, as Flink does with Kafka transactions).

## Today's build (`w13d4_streams.py`)

`WindowedCounter(n_partitions, window, max_out_of_order, allowed_lateness)`: `process`, `watermark`,
`emit`, `snapshot`, `restore`.

## Staff angle

The prompt "count ad clicks, 100 billion events/day, results in < 30 s" is this lab plus sizing.
State your three choices out loud: completeness (how long you wait = watermark bound), latency (when
you emit first), and cost of corrections (updates downstream, or a batch reconciliation job).
