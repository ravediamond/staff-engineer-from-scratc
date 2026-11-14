"""Self-contained. Run after predict.md."""
print("1. HW = min(10, 10, 7) = 7. Consumers see offsets 0..6.")
print("2. HW = min(10, 10) = 10: shrinking the ISR is how one slow replica stops blocking commits.")
print("3. The producer believes the record is stored. The new leader never had it: silent loss. acks=1 = leader-only durability.")
print("4. One failure with no loss (the record is on >= 2 replicas). Writes are refused when 2 are down (ISR = 1 < 2).")
print("5. Every broker restart drops the ISR to 2 < 3: acks=all producers get NotEnoughReplicas. min.insync = RF is a self-inflicted outage.")
