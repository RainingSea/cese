import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Dict
import os

class Expense:
    def __init__(self, amount: float, description: str, category: str):
        self.amount = amount
        self.description = description
        self.category = category

class ExpenseCategorizer:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories: List[str] = []
        self.load_expenses()
        self.load_categories()

    def add_expense(self, amount: float, description: str, category: str):
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()

    def load_expenses(self):
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split(',')
                    self.expenses.append(Expense(float(amount), description, category))

    def load_categories(self):
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                self.categories = [line.strip() for line in file]

    def save_expenses(self):
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.description},{expense.category}\n")

    def save_categories(self):
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category}\n")

    def categorize_expense(self, amount: float) -> str:
        # Simplified categorization logic
        return self.categories[0] if self.categories else "Uncategorized"

    def get_summary(self) -> Dict[str, float]:
        summary = {}
        for expense in self.expenses:
            if expense.category not in summary:
                summary[expense.category] = 0
            summary[expense.category] += expense.amount
        return summary

class ExpenseApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Expense Categorizer")
        self.categorizer = ExpenseCategorizer()
        
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()
        
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()
        
        self.category_var = tk.StringVar(value=self.categorizer.categories[0] if self.categorizer.categories else "")
        self.category_dropdown = ttk.Combobox(root, textvariable=self.category_var, values=self.categorizer.categories)
        self.category_dropdown.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.summary_button = tk.Button(root, text="Show Summary", command=self.show_summary)
        self.summary_button.pack()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_var.get()
            self.categorizer.add_expense(amount, description, category)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def show_summary(self):
        summary = self.categorizer.get_summary()
        summary_message = "\n".join([f"{category}: ${amount:.2f}" for category, amount in summary.items()])
        messagebox.showinfo("Expense Summary", summary_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()