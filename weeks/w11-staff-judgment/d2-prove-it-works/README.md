# W11 D2: prove it works (property-based testing with shrinking)

Primer: `knowledge/12-staff-rubrics.md` §3 ("Prove it works"). Reference: QuickCheck (Claessen & Hughes, 2000), Hypothesis.

## The one idea

"Prove it works" is pstack's first principle, and it is the habit that separates engineers whose
claims you can trust. Example-based tests check the cases you thought of. **Property-based tests**
state an invariant ("dedupe of a sorted list is sorted, has no duplicates, and has the same set of
elements") and throw hundreds of random inputs at it. When one fails, **shrinking** reduces it to a
minimal counterexample, which is usually the bug report you need.

Greedy shrinking: given a failing input, try smaller candidates; move to the first candidate that
**still fails**; repeat until no candidate fails. Return the last failing input.

| Type | Shrink candidates (in order) |
|---|---|
| int x | 0, x // 2 (toward 0), x − 1 if x > 0 else x + 1 (excluding x itself, deduplicated) |
| list xs | empty list, first half, second half, each single element removed, each element shrunk |

## Today's build (`w11d2_pbt.py`)

`gen_int(rng, lo, hi)`, `gen_list(rng, elem_gen, max_len)`, `shrink_int(x)`, `shrink_list(xs, shrink_elem)`,
`minimize(x, fails, shrinker)`, `check(prop, gen, shrinker, n, seed)` → `None` or the minimal counterexample.
Then use it to find a bug in a provided `dedupe_sorted_buggy`.

## Staff angle

Lauren's version of this is a "verification skill": a tool an agent (or a human) must run before saying
"done". The staff move is turning a habit into infrastructure: property tests in CI for core invariants,
equivalence tests for distributed code (W9), eval gates for model changes (W7). Then "prove it works"
stops depending on anyone's discipline.
