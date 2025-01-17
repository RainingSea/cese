import os
from expense import Expense

class ExpenseCategorizer:
    def __init__(self):
        self.expenses = []
        self.custom_categories = []
        self.load_expenses()
        self.load_categories()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()

    def load_expenses(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split(',')
                    self.expenses.append(Expense(float(amount), description, category))

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.description},{expense.category}\n")

    def load_categories(self) -> None:
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                self.custom_categories = [line.strip() for line in file]

    def save_categories(self) -> None:
        with open('categories.txt', 'w') as file:
            for category in self.custom_categories:
                file.write(f"{category}\n")

    def get_summary(self) -> dict:
        summary = {}
        for expense in self.expenses:
            if expense.category in summary:
                summary[expense.category] += expense.amount
            else:
                summary[expense.category] = expense.amount
        return summary