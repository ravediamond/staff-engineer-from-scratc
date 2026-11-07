"""Self-contained. Run after predict.md."""
m = 6 * 7e9 * 2.5e6 / (1000 * 990e12)
print(f"1. MFU = 6 x 7e9 x 2.5e6 / (1000 x 990e12) = {m:.1%}")
lost = 15 + 30  # restart + on average half an interval of redone work
print(f"2. per failure ~{lost} min lost (restart + half an interval redone) every 240 min -> ~{lost / 240:.0%} goodput loss")
print("3. it loads a checkpoint with a missing shard: crash at best, silently zero/garbage weights at worst")
