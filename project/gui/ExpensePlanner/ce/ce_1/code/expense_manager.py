from expense import Expense

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount: float, category: str) -> None:
        expense = Expense(amount, category)
        self.expenses.append(expense)

    def get_expenses(self):
        return self.expenses