# W3 D3: Lamport and vector clocks

Primer: `knowledge/03-distributed-systems.md` §3.

## The one idea

Wall clocks across machines disagree (NTP skew of milliseconds, sometimes seconds; leap smears;
VM pauses). Ordering events by wall time silently loses data (D2 predict #3). Logical clocks
order events by **causality** instead.

**Lamport clock:** one counter per process. Tick before each local event and send; on receive,
`c = max(c, received) + 1`. Guarantee: if A happened-before B then `L(A) < L(B)`. The converse is
false: `L(A) < L(B)` does not mean A caused B.

**Vector clock:** one counter **per process**, per process. On local event: increment your own
entry. On receive: element-wise max, then increment your own entry. Now you can tell:

| compare(a, b) | Condition |
|---|---|
| equal | all entries equal |
| before (a → b) | every `a[i] <= b[i]` and at least one `<` |
| after | the reverse |
| concurrent | some entry bigger on each side: **a conflict** |

Missing entries count as 0. Dynamo-style stores keep **siblings** (all concurrent versions) and
let the application merge (shopping cart = union).

## Today's build (`w3d3_clocks.py`)

- `LamportClock`: `tick()`, `send()`, `receive(ts)`.
- `vc_increment(vc, node)`, `vc_merge(a, b)`, `vc_compare(a, b)` on dicts (pure functions, return new dicts).
- `siblings(versions)`: given `[(vc, value), ...]`, keep only the versions not strictly before another (deduplicate equal clocks).

## Staff angle

Vector clocks grow with the number of writers; production systems bound them (Riak's dotted
version vectors, pruning). Most systems today avoid the problem instead: single leader per
partition (no concurrent writes), or CRDTs for data types that merge automatically (counters,
sets, text: Figma, Linear and collaborative editors). The staff move is to ask "do we need
multi-writer at all?" before choosing the clock.
