"""Review: a candidate's cost slide claimed the LLM bill dominates triage cost. Find the bug, fix it, explain:

WHY:
"""


def monthly_human_cost(tickets_per_day, escalation_rate, usd_per_ticket):
    return tickets_per_day * escalation_rate * usd_per_ticket
