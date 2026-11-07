"""Self-contained. Run after predict.md."""
print("1. the FIRST recorded output: wrong data, silently -> the replayed run is fiction")
print("2. 40 traces where behaviour changed at a tool call: exactly the cases to inspect. Not bad per se: it is the diff.")
print("3. side effects (emails, writes, payments) and non-determinism: replay must be hermetic")
