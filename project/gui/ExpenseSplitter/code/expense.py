class Expense:
    def __init__(self, total_amount: float, names: list):
        self.total_amount = total_amount
        self.names = names

    def calculate_share(self) -> float:
        if len(self.names) == 0:
            return 0.0
        return self.total_amount / len(self.names)

    def get_shares(self) -> dict:
        if not self.names:
            return {}
        share = self.calculate_share()
        return {name: share for name in self.names}