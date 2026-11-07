# Questions

1. Draw the state machine. Why is half-open needed at all?
2. Why split `allow()` from `record_*()` instead of only offering `call(fn)`?
3. Consecutive-failure threshold vs error-rate-over-window: when does each misbehave?
4. Your breaker opens on a dependency, and the product shows 500s. What did the design miss?
5. Breakers per instance vs shared across the fleet: trade-offs.

## Model answers

1. Closed → open on failures, open → half-open after a timeout, half-open → closed on enough successes or → open on any failure. Without half-open you either never retry (stay open forever) or flip straight to closed and dump full traffic on a service that may still be fragile.
2. Calls are concurrent and often async. Admission happens before the request, the outcome is known much later, and many calls overlap. Separating them lets you bound in-flight trials and integrate with async code, connection pools, or a service mesh.
3. Consecutive failures: simple, but at high traffic one success between failures keeps it closed even at 50% errors, and at low traffic 5 failures can take hours. Error rate over a window (with a minimum request count): robust at high traffic, but needs the minimum-volume guard or it trips on 1 of 1 failures.
4. A fallback. The breaker protects the dependency and the caller's resources, but the user still needs an answer: cached data, a degraded feature, a queue-and-notify, a cheaper model. Decide per dependency, in the design doc, before the incident.
5. Per instance: no coordination and independent views, but each instance learns separately (N instances × threshold failures) and instances flap independently. Shared (through a sidecar, mesh, or central store): faster consensus, but a new dependency and possible false global trips. Per-instance is the common default, with outlier detection in the mesh (Envoy) for per-host ejection.
