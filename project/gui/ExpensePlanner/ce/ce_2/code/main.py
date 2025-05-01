import tkinter as tk
from tkinter import messagebox
import json
import csv
from typing import List

class Expense:
    def __init__(self, amount: float, category: str, date: str, description: str) -> None:
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

class ExpenseManager:
    def __init__(self) -> None:
        self.expenses: List[Expense] = self.load_expenses()

    def add_expense(self, amount: float, category: str, date: str, description: str) -> None:
        expense = Expense(amount, category, date, description)
        self.expenses.append(expense)
        self.save_expenses()

    def get_expenses(self) -> List[Expense]:
        return self.expenses

    def load_expenses(self) -> List[Expense]:
        try:
            with open('expenses.json', 'r') as file:
                data = json.load(file)
                return [Expense(**item) for item in data]
        except FileNotFoundError:
            return []

    def save_expenses(self) -> None:
        with open('expenses.json', 'w') as file:
            json.dump([vars(expense) for expense in self.expenses], file)

class BudgetManager:
    def __init__(self) -> None:
        self.budget_goal = self.load_budget()

    def set_budget(self, goal: float) -> None:
        self.budget_goal = goal
        self.save_budget()

    def get_budget(self) -> float:
        return self.budget_goal

    def check_spending(self, expenses: List[Expense]) -> float:
        total_spent = sum(expense.amount for expense in expenses)
        return self.budget_goal - total_spent

    def load_budget(self) -> float:
        try:
            with open('budget.txt', 'r') as file:
                return float(file.read().strip())
        except FileNotFoundError:
            return 0.0

    def save_budget(self) -> None:
        with open('budget.txt', 'w') as file:
            file.write(str(self.budget_goal))

class Main:
    def __init__(self) -> None:
        self.expense_manager = ExpenseManager()
        self.budget_manager = BudgetManager()
        self.setup_ui()

    def setup_ui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Expense Planner")

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.budget_entry = tk.Entry(self.root)
        self.budget_entry.pack()

        self.set_budget_button = tk.Button(self.root, text="Set Budget", command=self.set_budget)
        self.set_budget_button.pack()

        self.check_button = tk.Button(self.root, text="Check Spending", command=self.check_spending)
        self.check_button.pack()

        self.root.mainloop()

    def add_expense(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get()
            description = self.description_entry.get()
            self.expense_manager.add_expense(amount, category, date, description)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")

    def set_budget(self) -> None:
        try:
            goal = float(self.budget_entry.get())
            self.budget_manager.set_budget(goal)
            messagebox.showinfo("Success", "Budget set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid budget!")

    def check_spending(self) -> None:
        remaining = self.budget_manager.check_spending(self.expense_manager.get_expenses())
        messagebox.showinfo("Spending Check", f"Remaining Budget: {remaining}")

if __name__ == "__main__":
    Main()