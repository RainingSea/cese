import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from datetime import datetime
import os

class Expense:
    def __init__(self, amount: float, category: str, date: str):
        self.amount = amount
        self.category = category
        self.date = date

class BudgetGoal:
    def __init__(self, category: str, amount: float):
        self.category = category
        self.amount = amount

class ExpensePlanner:
    def __init__(self):
        self.expenses = []
        self.budget_goals = {}
        self.load_data()

    def add_expense(self, amount: float, category: str, date: str) -> None:
        expense = Expense(amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def set_budget_goal(self, category: str, amount: float) -> None:
        self.budget_goals[category] = BudgetGoal(category, amount)
        self.save_data()

    def track_spending(self) -> dict:
        total_spent = {}
        for expense in self.expenses:
            if expense.category in total_spent:
                total_spent[expense.category] += expense.amount
            else:
                total_spent[expense.category] = expense.amount
        return total_spent

    def generate_report(self) -> str:
        report = "Category, Amount\n"
        for category, goal in self.budget_goals.items():
            spent = self.track_spending().get(category, 0)
            report += f"{category}, {spent}/{goal.amount}\n"
        return report

    def save_data(self) -> None:
        with open('expenses.txt', 'w') as exp_file:
            for expense in self.expenses:
                exp_file.write(f"{expense.amount}|{expense.category}|{expense.date}\n")
        
        with open('budget_goals.txt', 'w') as bg_file:
            for category, goal in self.budget_goals.items():
                bg_file.write(f"{category}|{goal.amount}\n")

    def load_data(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as exp_file:
                for line in exp_file:
                    amount, category, date = line.strip().split('|')
                    self.add_expense(float(amount), category, date)

        if os.path.exists('budget_goals.txt'):
            with open('budget_goals.txt', 'r') as bg_file:
                for line in bg_file:
                    category, amount = line.strip().split('|')
                    self.set_budget_goal(category, float(amount))

    def create_ui(self):
        root = tk.Tk()
        root.title("Expense Planner")

        tk.Label(root, text="Amount").grid(row=0, column=0)
        tk.Label(root, text="Category").grid(row=1, column=0)
        tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=2, column=0)

        amount_entry = tk.Entry(root)
        category_entry = tk.Entry(root)
        date_entry = tk.Entry(root)

        amount_entry.grid(row=0, column=1)
        category_entry.grid(row=1, column=1)
        date_entry.grid(row=2, column=1)

        def submit_expense():
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                date = date_entry.get()
                self.add_expense(amount, category, date)
                messagebox.showinfo("Success", "Expense added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid data.")

        submit_button = tk.Button(root, text="Submit Expense", command=submit_expense)
        submit_button.grid(row=3, columnspan=2)

        def generate_report():
            report = self.generate_report()
            messagebox.showinfo("Report", report)

        report_button = tk.Button(root, text="Generate Report", command=generate_report)
        report_button.grid(row=4, columnspan=2)

        root.mainloop()

if __name__ == "__main__":
    planner = ExpensePlanner()
    planner.create_ui()