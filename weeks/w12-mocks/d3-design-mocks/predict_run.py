"""Self-contained. Run after predict.md."""
print(f"1. {200e6 * 300 * 8 * 3 / 1e12:.2f} TB")
llm = 50_000 * 30 * (1500 * 1 + 200 * 5) / 1e6
human = 50_000 * 30 * 0.25 * 4
print(f"2. LLM ${llm:,.0f}/month, humans ${human:,.0f}/month -> humans dominate: optimise the escalation rate, not tokens")
