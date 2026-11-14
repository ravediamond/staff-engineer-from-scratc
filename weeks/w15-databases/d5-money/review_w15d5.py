"""Review: a wallet service.

WHY: amounts were binary floats. 0.1 + 0.2 is 0.30000000000000004 and three deposits of 0.10 give
0.30000000000000004 or 0.29999999999999993 depending on the order, so totals drift and "balance >= price"
fails by a rounding error. Money is stored as an integer number of the smallest unit (cents); conversion
from user input happens once, at the edge, with explicit rounding rules.
"""


class Wallets:
    def __init__(self):
        self.balance: dict[str, int] = {}

    @staticmethod
    def _check(cents) -> None:
        if type(cents) is not int or cents <= 0:
            raise ValueError("amount must be a positive integer number of cents")

    def deposit(self, user: str, cents: int) -> None:
        self._check(cents)
        self.balance[user] = self.balance.get(user, 0) + cents

    def pay(self, user: str, cents: int) -> bool:
        self._check(cents)
        if self.balance.get(user, 0) < cents:
            return False
        self.balance[user] -= cents
        return True
