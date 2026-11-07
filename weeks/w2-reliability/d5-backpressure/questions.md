# Questions

1. Define backpressure. Name three ways a system can apply it.
2. Little's law: state it, then use it to size a batch eval job against an API with 6 s p50 latency and 600 RPM limit.
3. Threads vs asyncio vs processes in Python for (a) 10k LLM API calls, (b) tokenizing 10 GB of text, (c) a mix.
4. Your 50M-document embedding backfill crashes at 60%. What should the design have included?
5. What goes wrong if you catch `asyncio.CancelledError` and do not re-raise it?

