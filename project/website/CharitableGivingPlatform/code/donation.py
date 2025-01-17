class Donation:
    def __init__(self, user: str, charity: str, amount: float, date: str):
        self.user = user
        self.charity = charity
        self.amount = amount
        self.date = date