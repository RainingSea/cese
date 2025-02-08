import os
from typing import List, Dict
from Expense import Expense

class ExpenseCategorizer:
    def __init__(self):
        self.categories: List[str] = []
        self.expenses: List[Dict] = []
        self.load_categories()
        self.load_expenses()

    def load_categories(self) -> None:
        """Load categories from the categories.txt file."""
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                self.categories = [line.strip() for line in file.readlines()]

    def save_categories(self) -> None:
        """Save categories to the categories.txt file."""
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category}\n")

    def add_expense(self, amount: float, description: str, category: str) -> None:
        """Add a new expense to the expenses list."""
        expense = Expense(amount, description, category)
        self.expenses.append({
            'amount': expense.amount,
            'description': expense.description,
            'category': expense.category
        })
        self.save_expenses()

    def save_expenses(self) -> None:
        """Save expenses to the expenses.txt file."""
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense['amount']},{expense['description']},{expense['category']}\n")

    def load_expenses(self) -> None:
        """Load expenses from the expenses.txt file."""
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split(',')
                    self.expenses.append({
                        'amount': float(amount),
                        'description': description,
                        'category': category
                    })

    def categorize_expenses(self) -> None:
        """Categorize expenses based on their categories."""
        categorized = {}
        for expense in self.expenses:
            category = expense['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(expense)
        return categorized

    def display_summary(self) -> str:
        """Display a summary of expenses categorized."""
        summary = ""
        categorized_expenses = self.categorize_expenses()
        for category, expenses in categorized_expenses.items():
            summary += f"Category: {category}\n"
            for expense in expenses:
                summary += f"  - {expense['description']}: ${expense['amount']}\n"
        return summary