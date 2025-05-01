class Expense:
    def __init__(self, amount: float, category: str):
        self.amount = amount
        self.category = category

    def get_details(self) -> str:
        return f"Expense: {self.amount} in category {self.category}"