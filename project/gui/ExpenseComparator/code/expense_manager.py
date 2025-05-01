import os
from expense import Expense
from typing import List

class ExpenseManager:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.file_path = 'expenses.txt'
        self.load_expenses()

    def add_expense(self, amount: float, category: str, date: str) -> Expense:
        expense = Expense(float(amount), category, date)
        self.expenses.append(expense)
        self.save_expenses()
        return expense

    def load_expenses(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    amount, category, date = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), category, date))

    def save_expenses(self):
        with open(self.file_path, 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount}|{expense.category}|{expense.date}\n")

    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Expense]:
        start = self.parse_date(start_date)
        end = self.parse_date(end_date)
        return [expense for expense in self.expenses if start <= self.parse_date(expense.date) <= end]

    def get_expenses_by_category(self, category: str) -> List[Expense]:
        return [expense for expense in self.expenses if expense.category == category]

    def visualize_expenses(self):
        category_totals = {}
        for expense in self.expenses:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
        return category_totals

    def parse_date(self, date_str: str):
        from datetime import datetime
        return datetime.strptime(date_str, '%Y-%m-%d')