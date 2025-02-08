class Expense:
    def __init__(self, amount: float, description: str, category: str) -> None:
        self.amount = amount
        self.description = description
        self.category = category