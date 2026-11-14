# Hands-on: the real tools, on your Mac

The labs simulate the mechanism. This folder makes you break the real thing the same way, so that in
an interview you speak from having typed the commands.

Rule: **simulate the invariant first (the lab), then reproduce the same failure on the real tool, and
write what you saw in the lab's `questions.md` notes.**

| Folder | After lab | Time |
|---|---|---|
| `kafka/` | W13 D3 | 2 × 1 h |
| `k8s/` | W14 D3 (core), W14 D4 (queues) | 3 × 1 h |

Setup once: Docker Desktop or Colima (`brew install colima docker docker-compose && colima start --cpu 4 --memory 8`),
then `brew install kind kubectl helm k9s kcat`.

**Honest note.** These guides were written from the official documentation and were NOT executed in the
environment that generated this repository (no Docker there). Image tags and manifest URLs change:
when a command fails, the linked documentation is the reference, and fixing it is part of the exercise.
Tell Claude what failed: tutor mode allows help here (this is not an exercise file).
