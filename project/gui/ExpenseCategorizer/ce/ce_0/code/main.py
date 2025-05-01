import tkinter as tk
from tkinter import messagebox
from typing import List

class Expense:
    def __init__(self, amount: float, description: str, category: str):
        self.amount = amount
        self.description = description
        self.category = category

class Category:
    def __init__(self, name: str):
        self.name = name

class ExpenseManager:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories: List[Category] = self.load_categories()

    def add_expense(self, amount: float, description: str, category: str):
        expense = Expense(amount, description, category)
        self.expenses.append(expense)
        self.save_expenses()

    def categorize_expenses(self):
        # This method could be expanded to categorize expenses automatically
        pass

    def get_summary(self) -> str:
        summary = {}
        for expense in self.expenses:
            if expense.category in summary:
                summary[expense.category] += expense.amount
            else:
                summary[expense.category] = expense.amount
        return "\n".join(f"{category}: {amount}" for category, amount in summary.items())

    def load_categories(self) -> List[Category]:
        categories = []
        try:
            with open('categories.txt', 'r') as file:
                for line in file:
                    categories.append(Category(line.strip()))
        except FileNotFoundError:
            pass
        return categories

    def save_expenses(self):
        with open('expenses.txt', 'a') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount}|{expense.description}|{expense.category}\n")

class Main:
    def __init__(self):
        self.expense_manager = ExpenseManager()
        self.create_ui()

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("Expense Categorizer")

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.summary_button = tk.Button(self.root, text="Show Summary", command=self.show_summary)
        self.summary_button.pack()

        self.summary_display = tk.Text(self.root)
        self.summary_display.pack()

        self.root.mainloop()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_entry.get()
            self.expense_manager.add_expense(amount, description, category)
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def show_summary(self):
        summary = self.expense_manager.get_summary()
        self.summary_display.delete(1.0, tk.END)
        self.summary_display.insert(tk.END, summary)

def main():
    app = Main()

if __name__ == "__main__":
    main()