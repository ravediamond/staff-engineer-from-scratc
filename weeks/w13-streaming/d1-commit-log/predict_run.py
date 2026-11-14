"""Self-contained. Run after predict.md."""
print("1. 3 segments: [0-3] [4-7] [8-9]; the active segment holds offsets 8 and 9.")
print("2. No. Retention and compaction never touch the active segment (segment.ms forces a roll first).")
print("3. Offsets 2 (k1,c) and 4 (k3,d). k2's tombstone removed the key (and is itself removed later).")
print("4. Offset 2: offsets never change. With offset 3 it would get the next existing record, offset 4.")
print(f"5. {2**30 // 4096:,} entries (a few MB, memory-mapped); at most ~4 KB of linear scan.")
