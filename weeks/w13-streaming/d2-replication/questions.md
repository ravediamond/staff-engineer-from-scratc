# Questions

1. Define LEO, HW and ISR. Why can a consumer not read above the HW?
2. Walk through the exact sequence in which `acks=1` loses an acknowledged record. Why does `acks=all` not have it?
3. What does `min.insync.replicas` add on top of `acks=all`? What goes wrong at 1, and at RF?
4. Unclean leader election: what is traded, and when would you turn it on?
5. Kafka tolerates f failures with f+1 replicas; Raft needs 2f+1. Where did the other f replicas go?
6. What did KRaft replace, since which version is it the only mode, and what does the controller quorum store?

## Model answers

1. LEO: the next offset a replica will write. ISR: the replicas that are alive and caught up with the leader within `replica.lag.time.max.ms`. HW: the minimum LEO across the ISR; records below it are on every in-sync replica (committed). Above the HW a record may exist on the leader only; if the leader fails, the new leader does not have it, so a consumer that had read it would have acted on data that then disappears, and two consumers could see different histories.
2. Producer sends; leader appends at offset n and acknowledges immediately; before any follower fetches n the leader crashes; a follower in the ISR becomes leader with LEO = n; the old leader, when it returns, truncates n. The producer holds an ack for a record that is in no log. With `acks=all` the ack is sent only once HW > n, i.e. every ISR member has n, so any electable leader has it.
3. `acks=all` means "all CURRENT in-sync replicas": if the ISR has shrunk to the leader alone, `all` is one replica. `min.insync.replicas` sets the floor below which such writes are refused. At 1 (the default) `acks=all` degrades silently to leader-only durability. At RF, any single broker restart or failure blocks writes. RF=3 with min ISR 2 is the standard.
4. Availability for durability and consistency: with no ISR member left, an out-of-sync replica becomes leader, the partition accepts traffic again, and every record it had not replicated is lost (the HW goes backwards, consumers may have seen records that vanish). Turn it on only where losing some data beats being down: metrics, logs, click streams with other sources of truth. Never for money or state changes.
5. Into the controller. Majority quorums embed membership agreement in every write. Kafka separates it: a small consensus group (the KRaft controller quorum, itself 2f+1) stores the leader, epoch and ISR of each partition; data replication then only needs the ISR members to all have the record, so any single survivor is a complete copy.
6. ZooKeeper. Kafka 4.0 (March 2025) is KRaft-only; 3.9 is the last release that can migrate from ZooKeeper. The controller quorum is a Raft-replicated metadata log holding topics, partitions, leaders, epochs, ISRs, configs, ACLs and broker registrations; brokers replay it instead of being pushed state by a single controller.
