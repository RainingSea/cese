import os
from datetime import datetime

class Expense:
    def __init__(self, date: str, amount: float, category: str):
        self.date = date
        self.amount = amount
        self.category = category

    def get_details(self) -> str:
        return f"{self.date}, {self.amount}, {self.category}"

class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.categories = self.load_categories()
        self.load_expenses()

    def load_categories(self):
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def load_expenses(self):
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file.readlines():
                    date, amount, category = line.strip().split(',')
                    self.expenses.append(Expense(date, float(amount), category))

    def add_expense(self, date: str, amount: float, category: str):
        new_expense = Expense(date, amount, category)
        self.expenses.append(new_expense)
        with open('expenses.txt', 'a') as file:
            file.write(new_expense.get_details() + "\n")

    def get_expenses(self, start_date: str, end_date: str):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return [expense for expense in self.expenses if start <= datetime.strptime(expense.date, '%Y-%m-%d') <= end]

    def visualize_expenses(self):
        categories = {}
        for expense in self.expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount
        
        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.title('Expenses by Category')
        plt.show()