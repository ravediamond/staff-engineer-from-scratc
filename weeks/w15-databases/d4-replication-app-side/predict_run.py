"""Self-contained. Run after predict.md."""
print("1. The old profile: their own write has not reached the replica. (Read-your-writes violation.)")
print("2. Only the replica at 100 (>= 95). If none qualifies, read from the primary.")
print("3. 8 (LSN 113-120): acknowledged to clients, never shipped. RPO = replication lag at the time of failure.")
print("4. 0: the primary does not acknowledge before the replica has the write.")
print("5. Split brain. Fencing: the old primary must be unable to accept writes (lease/epoch checked by storage or clients, STONITH).")
