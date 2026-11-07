# W3 D2: quorum replication, read repair

Primer: `knowledge/03-distributed-systems.md` §2.

## The one idea

Store each key on **N** replicas. A write succeeds when **W** replicas acknowledge; a read asks
**R** replicas and returns the value with the **highest version**. If **R + W > N**, every read
quorum overlaps every write quorum in at least one replica, so a read sees the latest acknowledged
write (assuming versions order writes correctly, and no sloppy quorums).

| N, R, W | Property |
|---|---|
| 3, 2, 2 | overlap: read-your-latest-write; tolerates 1 failure for both reads and writes |
| 3, 1, 3 | fast reads, writes need all replicas up |
| 3, 1, 1 | fast and available, **stale reads possible** (R + W = 2 ≤ 3) |

**Read repair:** the coordinator saw which replicas returned old versions, so it writes the newest
version back to them. Anti-entropy (Merkle trees) repairs keys that nobody reads.

Today versions are timestamps provided by the client (last-writer-wins). D3 shows why that is
dangerous and what vector clocks give instead.

## Today's build (`w3d2_quorum.py`)

- `Cluster(n, r, w)` with replicas `0..n-1`, a `down` set.
- `put(key, value, version, targets=None)`: writes to `targets` (default all up replicas); partial writes
  persist; raises `QuorumError` if fewer than W up targets acknowledged.
- `get(key, sources=None)`: reads from `sources` (default the first R up replicas); `QuorumError` if fewer than R;
  returns the highest-version value (None if absent); read-repairs stale or missing replicas among the sources.
- `overlaps(n, r, w)`.

## Staff angle

R + W > N is necessary, not sufficient, for linearizability: concurrent writes, clock skew in
LWW versions, and sloppy quorums (hinted handoff writing to non-home nodes during partitions)
all break it. A staff answer states the actual guarantee ("read-your-writes for a single client
with monotonic versions, not linearizable"), then asks whether the product needs more. Most
features do not; payments and leader election do, and those go through consensus (D4).
