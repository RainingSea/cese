import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class Expense:
    def __init__(self, amount: float, description: str, category: str):
        self.amount = amount
        self.description = description
        self.category = category

class BudgetGoal:
    def __init__(self, category: str, amount: float):
        self.category = category
        self.amount = amount

class ExpensePlanner:
    def __init__(self):
        self.expenses = []
        self.budget_goals = []
        self.load_data()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()
        messagebox.showinfo("Success", "Expense added successfully!")

    def set_budget_goal(self, category: str, amount: float) -> None:
        budget_goal = BudgetGoal(category, amount)
        self.budget_goals.append(budget_goal)
        self.save_budget_goals()
        messagebox.showinfo("Success", "Budget goal set successfully!")

    def generate_report(self) -> str:
        report = "Expense Report:\n"
        total_expense = 0
        for expense in self.expenses:
            report += f"{expense.description}: ${expense.amount} in {expense.category}\n"
            total_expense += expense.amount
        report += f"Total Expenses: ${total_expense}"
        self.save_report(report)
        return report

    def visualize_budget(self) -> None:
        categories = [goal.category for goal in self.budget_goals]
        amounts = [goal.amount for goal in self.budget_goals]
        plt.pie(amounts, labels=categories, autopct='%1.1f%%')
        plt.title("Budget Breakdown")
        plt.show()

    def load_data(self) -> None:
        try:
            with open('expenses.txt', 'r') as f:
                for line in f:
                    amount, description, category = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), description, category))
        except FileNotFoundError:
            pass

        try:
            with open('budget_goals.txt', 'r') as f:
                for line in f:
                    category, amount = line.strip().split('|')
                    self.budget_goals.append(BudgetGoal(category, float(amount)))
        except FileNotFoundError:
            pass

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as f:
            for expense in self.expenses:
                f.write(f"{expense.amount}|{expense.description}|{expense.category}\n")

    def save_budget_goals(self) -> None:
        with open('budget_goals.txt', 'w') as f:
            for goal in self.budget_goals:
                f.write(f"{goal.category}|{goal.amount}\n")

    def save_report(self, report: str) -> None:
        with open('reports.txt', 'w') as f:
            f.write(report)

def main():
    root = tk.Tk()
    root.title("Expense Planner")
    planner = ExpensePlanner()

    # UI Components
    amount_label = tk.Label(root, text="Amount:")
    amount_label.grid(row=0, column=0)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=0, column=1)

    description_label = tk.Label(root, text="Description:")
    description_label.grid(row=1, column=0)
    description_entry = tk.Entry(root)
    description_entry.grid(row=1, column=1)

    category_label = tk.Label(root, text="Category:")
    category_label.grid(row=2, column=0)
    category_entry = tk.Entry(root)
    category_entry.grid(row=2, column=1)

    def add_expense_action():
        amount = float(amount_entry.get())
        description = description_entry.get()
        category = category_entry.get()
        planner.add_expense(amount, description, category)

    add_expense_button = tk.Button(root, text="Add Expense", command=add_expense_action)
    add_expense_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()