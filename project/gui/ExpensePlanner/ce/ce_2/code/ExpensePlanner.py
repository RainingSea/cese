import os
from typing import List, Dict
from Expense import Expense

class ExpensePlanner:
    def __init__(self) -> None:
        self.expenses: List[Expense] = []
        self.budget_goals: Dict[str, float] = {}
        self.load_data()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_data()

    def set_budget(self, category: str, budget_amount: float) -> None:
        self.budget_goals[category] = budget_amount
        self.save_data()

    def load_data(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split(',')
                    self.add_expense(float(amount), description, category)

        if os.path.exists('budget.txt'):
            with open('budget.txt', 'r') as file:
                for line in file:
                    category, budget_amount = line.strip().split(',')
                    self.set_budget(category, float(budget_amount))

    def save_data(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.description},{expense.category}\n")

        with open('budget.txt', 'w') as file:
            for category, budget_amount in self.budget_goals.items():
                file.write(f"{category},{budget_amount}\n")

    def generate_report(self) -> str:
        report = "Expense Report:\n"
        for category in self.budget_goals:
            total_expense = sum(exp.amount for exp in self.expenses if exp.category == category)
            report += f"Category: {category}, Budget: {self.budget_goals[category]}, Total Expenses: {total_expense}\n"
        return report