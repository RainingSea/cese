class Expense:
    def __init__(self, amount: float, participants: list):
        self.amount = amount
        self.participants = participants

    def get_share(self) -> dict:
        share = self.amount / len(self.participants)
        return {participant: share for participant in self.participants}