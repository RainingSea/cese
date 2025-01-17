import os
from Expense import Expense
from Category import Category

class ExpenseCategorizer:
    def __init__(self):
        self.expenses = []
        self.categories = []
        self.load_data()

    def add_expense(self, amount: float, category: str, date: str) -> None:
        expense = Expense(amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def categorize_expenses(self) -> None:
        # This method can be expanded for categorization logic
        pass

    def create_category(self, name: str) -> None:
        category = Category(name)
        self.categories.append(category)
        self.save_data()

    def get_summary(self) -> dict:
        summary = {}
        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = 0
            summary[expense.category] += expense.amount
        return summary

    def load_data(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, category, date = line.strip().split(',')
                    self.add_expense(float(amount), category, date)
        
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                for line in file:
                    name = line.strip()
                    self.create_category(name)

    def save_data(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.category},{expense.date}\n")
        
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category.name}\n")