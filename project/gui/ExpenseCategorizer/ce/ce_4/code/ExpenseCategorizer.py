import csv
from typing import List, Dict
from Expense import Expense

class ExpenseCategorizer:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories: List[str] = []
        self.load_expenses()
        self.load_categories()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        amount = float(row[0])
                        description = row[1]
                        category = row[2]
                        self.expenses.append(Expense(amount, description, category))
        except FileNotFoundError:
            pass

    def load_categories(self) -> None:
        try:
            with open('categories.txt', 'r') as file:
                reader = csv.reader(file)
                self.categories = [row[0] for row in reader if row]
        except FileNotFoundError:
            pass

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            for expense in self.expenses:
                writer.writerow([expense.amount, expense.description, expense.category])

    def save_categories(self) -> None:
        with open('categories.txt', 'w', newline='') as file:
            writer = csv.writer(file)
            for category in self.categories:
                writer.writerow([category])

    def get_summary(self) -> Dict[str, float]:
        summary = {}
        for expense in self.expenses:
            if expense.category in summary:
                summary[expense.category] += expense.amount
            else:
                summary[expense.category] = expense.amount
        return summary