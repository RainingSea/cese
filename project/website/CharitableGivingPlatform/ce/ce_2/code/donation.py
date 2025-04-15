class Donation:
    def __init__(self, user, charity, amount: float, date: str):
        self.user = user
        self.charity = charity
        self.amount = amount
        self.date = date