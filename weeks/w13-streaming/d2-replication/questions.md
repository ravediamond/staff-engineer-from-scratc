# Questions

1. Define LEO, HW and ISR. Why can a consumer not read above the HW?
2. Walk through the exact sequence in which `acks=1` loses an acknowledged record. Why does `acks=all` not have it?
3. What does `min.insync.replicas` add on top of `acks=all`? What goes wrong at 1, and at RF?
4. Unclean leader election: what is traded, and when would you turn it on?
5. Kafka tolerates f failures with f+1 replicas; Raft needs 2f+1. Where did the other f replicas go?
6. What did KRaft replace, since which version is it the only mode, and what does the controller quorum store?

