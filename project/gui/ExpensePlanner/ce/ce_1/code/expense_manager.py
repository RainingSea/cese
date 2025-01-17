import json
from typing import List

class Expense:
    def __init__(self, amount: float, category: str, date: str):
        self.amount = amount
        self.category = category
        self.date = date

class Category:
    def __init__(self, name: str):
        self.name = name

class BudgetGoal:
    def __init__(self, category: str, amount: float):
        self.category = category
        self.amount = amount

class ExpensePlanner:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories: List[Category] = []
        self.budget_goals: List[BudgetGoal] = []
        self.load_data()

    def add_expense(self, amount: float, category: str, date: str):
        expense = Expense(amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def set_budget_goal(self, category: str, amount: float):
        budget_goal = BudgetGoal(category, amount)
        self.budget_goals.append(budget_goal)
        self.save_data()

    def generate_report(self) -> str:
        report = "Expense Report:\n"
        for expense in self.expenses:
            report += f"{expense.date}: {expense.category} - ${expense.amount:.2f}\n"
        return report

    def visualize_budget_breakdown(self):
        # Visualization logic will be implemented in visualization.py
        pass

    def load_data(self):
        try:
            with open('expenses.txt', 'r') as f:
                for line in f:
                    amount, category, date = line.strip().split('|')
                    self.add_expense(float(amount), category, date)
            with open('budget_goals.txt', 'r') as f:
                for line in f:
                    category, amount = line.strip().split('|')
                    self.set_budget_goal(category, float(amount))
            with open('categories.txt', 'r') as f:
                for line in f:
                    name = line.strip()
                    self.categories.append(Category(name))
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('expenses.txt', 'w') as f:
            for expense in self.expenses:
                f.write(f"{expense.amount}|{expense.category}|{expense.date}\n")
        with open('budget_goals.txt', 'w') as f:
            for goal in self.budget_goals:
                f.write(f"{goal.category}|{goal.amount}\n")
        with open('categories.txt', 'w') as f:
            for category in self.categories:
                f.write(f"{category.name}\n")