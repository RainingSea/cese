import tkinter as tk
from tkinter import messagebox
from typing import List
import os

class Expense:
    def __init__(self, amount: float, description: str, category: str):
        self.amount = amount
        self.description = description
        self.category = category

class ExpenseCategorizer:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories: List[str] = self.load_categories()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()
    
    def categorize_expenses(self) -> None:
        # Placeholder for future categorization logic
        pass

    def create_custom_category(self, category: str) -> None:
        if category not in self.categories:
            self.categories.append(category)
            self.save_categories()
    
    def get_expense_summary(self) -> str:
        summary = {}
        for expense in self.expenses:
            if expense.category in summary:
                summary[expense.category] += expense.amount
            else:
                summary[expense.category] = expense.amount
        return '\n'.join([f"{cat}: {amt}" for cat, amt in summary.items()])

    def load_expenses(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split(',')
                    self.add_expense(float(amount), description, category)

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount},{expense.description},{expense.category}\n")

    def load_categories(self) -> List[str]:
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def save_categories(self) -> None:
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category}\n")

class ExpenseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Categorizer")
        self.categorizer = ExpenseCategorizer()
        self.categorizer.load_expenses()

        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack()

        self.description_entry = tk.Entry(master)
        self.description_entry.pack()

        self.category_var = tk.StringVar(master)
        self.category_var.set(self.categorizer.categories[0] if self.categorizer.categories else "")
        self.category_menu = tk.OptionMenu(master, self.category_var, *self.categorizer.categories)
        self.category_menu.pack()

        self.add_button = tk.Button(master, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.summary_button = tk.Button(master, text="Show Summary", command=self.show_summary)
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
        summary = self.categorizer.get_expense_summary()
        messagebox.showinfo("Expense Summary", summary if summary else "No expenses recorded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()