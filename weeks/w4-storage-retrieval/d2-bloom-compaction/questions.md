# Questions

1. Why can a Bloom filter have false positives but never false negatives?
2. Derive bits per key for 1% from the formula (or explain where 9.6 comes from).
3. Why can't you delete from a standard Bloom filter? What can you use instead?
4. Leveled vs size-tiered compaction: which reduces read amplification, which reduces write amplification?
5. You must deduplicate a 2B-document crawl for pretraining or RAG. Which probabilistic structures and how?

## Model answers

1. A member always set all k of its bits, so they all read 1 (no false negatives). A non-member's k bits may have been set by other items (false positive).
2. With optimal k = (m/n)ln 2, p = (1/2)^k = e^(-(m/n)(ln 2)^2), so m/n = -ln p / (ln 2)^2 = 4.605 / 0.4805 ≈ 9.58 bits per key.
3. Clearing a bit may remove other items' bits and create false negatives. Use a counting Bloom filter (counters instead of bits, about 4× memory), a cuckoo filter (supports delete, good space at low p), or rebuild periodically.
4. Leveled (LevelDB/RocksDB default): few overlapping runs per level gives lower read and space amplification but higher write amplification. Size-tiered (Cassandra default): merges similar-sized runs, lower write amplification, higher read and space amplification.
5. Exact duplicates: hash normalized text (SHA-1/xxhash) into a distributed set, or a Bloom filter as a first-pass filter. Near-duplicates: MinHash signatures over shingles plus LSH banding to find candidate pairs above a Jaccard threshold (e.g. 0.8), then union-find to cluster and keep one per cluster. Run it as a MapReduce/Spark job, and report the dedup rate per source.
