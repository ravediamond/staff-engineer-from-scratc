"""Self-contained. Run after predict.md."""
print("1. B-tree: each random write dirties a 4 KB page -> up to ~40x amplification at ingest. LSM: sequential appends,")
print("   amplification comes later from compaction (typically 10-30x over the data's life, but sequential).")
print("2. All 10 (memtable + every SSTable) -> why bloom filters: ~1% false positives -> ~0.1 file reads per miss.")
print("3. Skip it: a torn tail is an incomplete, never-acknowledged write. A corrupt line in the MIDDLE means real corruption -> fail loudly.")
