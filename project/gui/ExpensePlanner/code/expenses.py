import os
from datetime import datetime

class Expense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = datetime.now().strftime("%Y-%m-%d")

class ExpenseManager:
    def __init__(self):
        self.expenses = []

    def add_expense(self, amount: float, category: str, description: str) -> None:
        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_expenses()

    def load_expenses(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, category, description, date = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), category, description))

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount}|{expense.category}|{expense.description}|{expense.date}\n")

    def remove_expense(self, index: int) -> None:
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()