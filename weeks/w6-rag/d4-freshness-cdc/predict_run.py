"""Self-contained. Run after predict.md."""
print("1. last event wins: upsert v2 -> the deleted document is BACK (and with stale content)")
print("2. removal: after delete there is no stored version, so v2 looks new -> resurrected again")
print("3. tombstone v3 > v2 -> late upsert ignored -> doc stays deleted")
