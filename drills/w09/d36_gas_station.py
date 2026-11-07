"""d36 Gas station: circular route, gas[i] at station i, cost[i] to go to i+1. Return the unique start index
that completes the circuit, or -1."""


def can_complete(gas: list, cost: list) -> int:
    if sum(gas) < sum(cost):
        return -1
    start = tank = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start, tank = i + 1, 0
    return start
