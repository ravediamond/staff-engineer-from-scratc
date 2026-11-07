"""Review: agent loop from a teammate. A customer's run was billed for one more tool call than their plan allows.
Find the bug, fix it, explain:

WHY:
"""


def run(model, execute, max_steps):
    steps, trace = 0, []
    while True:
        if steps >= max_steps:
            return "max_steps", trace
        action = model(trace)
        if "final" in action:
            return action["final"], trace
        trace.append(execute(action))
        steps += 1
