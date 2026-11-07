"""Self-contained. Run after predict.md."""
print("1. Lease expired at +10 s; anyone may hold it now. The client cannot tell from its own clock.")
print("2. No: Redlock bounds who gets the lease, but a paused holder still writes after expiry. Needs fencing at the resource.")
print("3. '>=' lets the current holder write many times with the same token; '>' would reject its second write.")
