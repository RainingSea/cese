class Expense:
    def __init__(self, amount: float, category: str, date: str):
        self.amount = amount
        self.category = category
        self.date = date

    def get_details(self):
        return f"{self.date}, {self.amount}, {self.category}"