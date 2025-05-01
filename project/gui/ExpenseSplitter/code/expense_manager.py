import os
import json
from expense import Expense

class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)
        self.save_expenses()

    def load_expenses(self) -> None:
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as file:
                data = json.load(file)
                for entry in data:
                    total_amount = entry['total']
                    names = entry['names']
                    expense = Expense(total_amount, names)
                    self.expenses.append(expense)

    def save_expenses(self) -> None:
        with open('expenses.json', 'w') as file:
            data = [{'total': expense.total_amount, 'names': expense.names} for expense in self.expenses]
            json.dump(data, file)

    def calculate_shares(self) -> dict:
        shares = {}
        for expense in self.expenses:
            shares.update(expense.get_shares())
        return shares