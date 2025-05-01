import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from datetime import datetime
from typing import List

class Expense:
    def __init__(self, date: str, category: str, amount: float):
        self.date = date
        self.category = category
        self.amount = amount

class ExpenseManager:
    def __init__(self):
        self.expenses = self.load_expenses()

    def load_expenses(self) -> List[Expense]:
        expenses = []
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    date, category, amount = line.strip().split(',')
                    expenses.append(Expense(date, category, float(amount)))
        except FileNotFoundError:
            with open('expenses.txt', 'w') as file:
                pass  # Create the file if it doesn't exist
        return expenses

    def add_expense(self, date: str, category: str, amount: float) -> None:
        new_expense = Expense(date, category, amount)
        self.expenses.append(new_expense)
        with open('expenses.txt', 'a') as file:
            file.write(f"{date},{category},{amount}\n")

    def get_expenses(self, start_date: str, end_date: str) -> List[Expense]:
        return [
            expense for expense in self.expenses
            if start_date <= expense.date <= end_date
        ]

    def visualize_expenses(self) -> None:
        categories = {}
        for expense in self.expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Categories')
        plt.ylabel('Total Amount')
        plt.title('Expenses by Category')
        plt.show()

class Main:
    def __init__(self):
        self.expense_manager = ExpenseManager()
        self.window = tk.Tk()
        self.window.title("Expense Comparator")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.window)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.window, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.window)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.window, text="Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.grid(row=2, column=1)

        tk.Button(self.window, text="Add Expense", command=self.add_expense).grid(row=3, columnspan=2)
        tk.Button(self.window, text="Visualize Expenses", command=self.expense_manager.visualize_expenses).grid(row=4, columnspan=2)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if not date or not category or not amount:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            amount = float(amount)
            self.expense_manager.add_expense(date, category, amount)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.date_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number.")

    def main(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()