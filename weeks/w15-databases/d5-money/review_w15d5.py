"""Review: a wallet service. The nightly check "sum of all wallets == money received" fails by a few cents
every day, and one customer could not spend their last 0.30. Find the bug, fix it, explain:

WHY:
"""


class Wallets:
    def __init__(self):
        self.balance: dict[str, float] = {}

    def deposit(self, user: str, euros: float) -> None:
        self.balance[user] = self.balance.get(user, 0.0) + euros

    def pay(self, user: str, euros: float) -> bool:
        if self.balance.get(user, 0.0) < euros:
            return False
        self.balance[user] -= euros
        return True
