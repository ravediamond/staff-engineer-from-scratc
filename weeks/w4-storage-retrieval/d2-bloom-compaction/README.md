# W4 D2: bloom filters and compaction

Primer: `knowledge/04-storage-and-retrieval.md` §2.

## The one idea

**Bloom filter:** a bit array of size m and k hash functions. `add(x)` sets k bits;
`might_contain(x)` checks them. **No false negatives, tunable false positives.** One per SSTable
lets a read skip files that certainly do not contain the key.

Math you should be able to write on a whiteboard:

- false positive rate `p ≈ (1 - e^(-k·n/m))^k`
- optimal `m = -n·ln(p) / (ln 2)²` → about **9.6 bits per key for 1%**, 14.4 for 0.1%
- optimal `k = (m/n)·ln 2`
- k hashes from 2 (Kirsch–Mitzenmacher): `h_i = h1 + i·h2 mod m`

**Compaction:** merge several sorted runs into one, keeping only the **newest** version of each key
(runs are ordered newest first), and dropping tombstones when merging into the bottom level. A
k-way merge of sorted runs is a heap problem (`heapq.merge`), O(total · log k).

## Today's build (`w4d2_bloom.py`)

- `optimal_params(n, p) -> (m, k)` (ceil m, round k, k ≥ 1), `false_positive_rate(m, n, k)`.
- `BloomFilter(m, k)`: `add`, `might_contain`, double hashing on SHA-256.
- `compact(runs, drop_tombstones)`: runs newest first, each a sorted list of `(key, value)`; output one sorted run.

## Staff angle

Probabilistic structures are the staff engineer's favourite cost lever: Bloom filters (skip I/O),
HyperLogLog (count distinct users in 12 KB), Count-Min (heavy hitters), MinHash/LSH
(near-duplicate detection: exactly how you dedupe a pretraining or RAG corpus). In interviews,
offering "an approximate answer at 1/1000th the cost, with a stated error bound" is a strong
signal, provided you state the error bound and who can tolerate it.
