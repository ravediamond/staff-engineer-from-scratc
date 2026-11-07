"""Self-contained. Run after predict.md."""
print("1. one bin: |0.70 - 0.95| = 0.25 ECE (overconfident)")
print("2. no: sigma(m/T) is monotonic in m, so the sign of every margin and the ranking are unchanged")
print("3. yes: the RM pays for length itself. Optimising against it (BoN, RL) will inflate answer length.")
