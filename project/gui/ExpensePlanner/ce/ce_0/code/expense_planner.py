import json
from expense import Expense

class ExpensePlanner:
    def __init__(self):
        self.expenses = []
        self.budget_goals = {}

    def add_expense(self, amount: float, category: str) -> None:
        date = self.get_current_date()
        new_expense = Expense(amount, category, date)
        self.expenses.append(new_expense)
        self.save_data()

    def set_budget_goal(self, category: str, amount: float) -> None:
        self.budget_goals[category] = amount
        self.save_data()

    def track_spending(self) -> dict:
        spending_summary = {}
        for expense in self.expenses:
            if expense.category in spending_summary:
                spending_summary[expense.category] += expense.amount
            else:
                spending_summary[expense.category] = expense.amount
        return spending_summary

    def generate_report(self) -> str:
        report = "Expense Report:\n"
        for expense in self.expenses:
            report += f"{expense.date}: {expense.category} - ${expense.amount:.2f}\n"
        return report

    def visualize_budget(self) -> None:
        import matplotlib.pyplot as plt

        categories = list(self.budget_goals.keys())
        amounts = list(self.budget_goals.values())

        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Budget Amounts')
        plt.title('Budget Visualization')
        plt.show()

    def load_data(self) -> None:
        try:
            with open('expenses.txt', 'r') as f:
                for line in f:
                    amount, category, date = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), category, date))
        except FileNotFoundError:
            pass

        try:
            with open('budget_goals.txt', 'r') as f:
                for line in f:
                    category, amount = line.strip().split('|')
                    self.budget_goals[category] = float(amount)
        except FileNotFoundError:
            pass

    def save_data(self) -> None:
        with open('expenses.txt', 'w') as f:
            for expense in self.expenses:
                f.write(f"{expense.amount}|{expense.category}|{expense.date}\n")

        with open('budget_goals.txt', 'w') as f:
            for category, amount in self.budget_goals.items():
                f.write(f"{category}|{amount}\n")

    def get_current_date(self) -> str:
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")