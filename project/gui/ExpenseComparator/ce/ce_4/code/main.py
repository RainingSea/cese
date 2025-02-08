import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from typing import List

class Expense:
    def __init__(self, amount: float, category: str, date: str):
        self.amount = amount
        self.category = category
        self.date = date

class ExpenseComparator:
    def __init__(self):
        self.expenses = []
        self.categories = []
        self.load_data()

    def add_expense(self, amount: float, category: str, date: str):
        expense = Expense(amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def get_expenses(self, start_date: str, end_date: str) -> List[Expense]:
        return [expense for expense in self.expenses if start_date <= expense.date <= end_date]

    def generate_report(self, start_date: str, end_date: str) -> dict:
        report = {}
        for expense in self.get_expenses(start_date, end_date):
            if expense.category not in report:
                report[expense.category] = 0
            report[expense.category] += expense.amount
        return report

    def load_data(self):
        try:
            with open('expenses.json', 'r') as f:
                data = json.load(f)
                self.expenses = [Expense(**item) for item in data]
        except FileNotFoundError:
            self.expenses = []

        try:
            with open('categories.txt', 'r') as f:
                self.categories = f.read().splitlines()
        except FileNotFoundError:
            self.categories = []

    def save_data(self):
        with open('expenses.json', 'w') as f:
            json.dump([expense.__dict__ for expense in self.expenses], f)

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Comparator")
        self.comparator = ExpenseComparator()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)

        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        tk.Label(root, text="Amount:").grid(row=0, column=0)
        tk.Label(root, text="Category:").grid(row=1, column=0)
        tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=2, column=0)

        self.submit_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=3, columnspan=2)

        self.report_button = tk.Button(root, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=4, columnspan=2)

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get()
        self.comparator.add_expense(amount, category, date)
        messagebox.showinfo("Success", "Expense added successfully!")

    def generate_report(self):
        start_date = self.date_entry.get()
        end_date = self.date_entry.get()
        report = self.comparator.generate_report(start_date, end_date)
        report_str = "\n".join(f"{category}: {amount}" for category, amount in report.items())
        messagebox.showinfo("Report", report_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()