import tkinter as tk
from tkinter import messagebox
from typing import List

class Expense:
    def __init__(self, amount: float, description: str, category: str) -> None:
        self.amount = amount
        self.description = description
        self.category = category

class Category:
    def __init__(self, name: str) -> None:
        self.name = name

class ExpenseManager:
    def __init__(self) -> None:
        self.expenses: List[Expense] = []
        self.categories: List[Category] = self.load_categories()
        self.load_expenses()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if category not in [cat.name for cat in self.categories]:
            raise ValueError("Category does not exist.")
        self.expenses.append(Expense(amount, description, category))
        self.categorize_expense(description, amount)
        self.save_expenses()

    def categorize_expense(self, description: str, amount: float) -> None:
        keywords = {
            'Food': ['lunch', 'dinner', 'groceries', 'snack'],
            'Transport': ['taxi', 'bus', 'train', 'transport'],
            'Utilities': ['electricity', 'water', 'internet'],
            'Entertainment': ['movie', 'concert', 'game'],
            'Travel': ['flight', 'hotel', 'trip']
        }
        for category, words in keywords.items():
            if any(word in description.lower() for word in words):
                self.create_custom_category(category)
                return

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), description, category))
        except FileNotFoundError:
            pass

    def load_categories(self) -> List[Category]:
        categories = []
        try:
            with open('categories.txt', 'r') as file:
                for line in file:
                    categories.append(Category(line.strip()))
        except FileNotFoundError:
            pass
        return categories

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount}|{expense.description}|{expense.category}\n")

    def save_categories(self) -> None:
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category.name}\n")

    def create_custom_category(self, category: str) -> None:
        if category not in [cat.name for cat in self.categories]:
            self.categories.append(Category(category))
            self.save_categories()

    def get_summary(self) -> str:
        summary = {}
        for expense in self.expenses:
            if expense.category in summary:
                summary[expense.category] += expense.amount
            else:
                summary[expense.category] = expense.amount
        return "\n".join(f"{cat}: {amt}" for cat, amt in summary.items())

class Main:
    def __init__(self) -> None:
        self.expense_manager = ExpenseManager()
        self.create_gui()

    def create_gui(self) -> None:
        self.root = tk.Tk()
        self.root.title("Expense Categorizer")

        tk.Label(self.root, text="Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Description:").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Category:").grid(row=2, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.summary_button = tk.Button(self.root, text="Show Summary", command=self.show_summary)
        self.summary_button.grid(row=4, column=0, columnspan=2)

        self.summary_display = tk.Text(self.root, height=10, width=30)
        self.summary_display.grid(row=5, column=0, columnspan=2)

        self.root.mainloop()

    def add_expense(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_entry.get()
            self.expense_manager.add_expense(amount, description, category)
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_summary(self) -> None:
        summary = self.expense_manager.get_summary()
        self.summary_display.delete(1.0, tk.END)
        self.summary_display.insert(tk.END, summary)