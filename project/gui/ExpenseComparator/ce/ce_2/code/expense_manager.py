from typing import List

class Expense:
    def __init__(self, date: str, amount: float, category: str):
        self.date = date
        self.amount = amount
        self.category = category

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date: str, amount: float, category: str) -> None:
        expense = Expense(date, amount, category)
        self.expenses.append(expense)

    def get_expenses(self, start_date: str, end_date: str) -> List[Expense]:
        return [expense for expense in self.expenses if start_date <= expense.date <= end_date]