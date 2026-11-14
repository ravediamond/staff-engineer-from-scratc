"""Self-contained. Run after predict.md."""
print("1. After the event at 71: watermark = 71 - 10 = 61 >= 60. (At 62 the watermark is 52. The event at 58 is counted.)")
print("2. min(500 - 10, 90 - 10) = 80. The slow partition holds the watermark.")
print("3. At 75: counted (75 < 60 + 30), and the window fires again with the new count. At 95: too late -> side output.")
print("4. Offsets 60-99. The restored state reflects exactly offsets 0-59, so replaying 60-99 counts each event once.")
print(f"5. {100e9 / 86400:,.0f} events/s on average, about {3 * 100e9 / 86400 / 1e6:.1f} M/s at peak.")
