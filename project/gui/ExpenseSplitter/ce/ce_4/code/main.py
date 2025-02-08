import tkinter as tk
from tkinter import messagebox
import os

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.shares = {}

        self.load_expenses()
        self.load_shares()

    def add_expense(self, amount: float, names: list):
        self.expenses.append((amount, names))
        self.calculate_shares()

    def calculate_shares(self) -> dict:
        total_expense = sum(expense[0] for expense in self.expenses)
        total_people = sum(len(expense[1]) for expense in self.expenses)

        if total_people == 0:
            return {}

        share_amount = total_expense / total_people
        self.shares = {name: share_amount for expense in self.expenses for name in expense[1]}
        self.save_shares()
        return self.shares

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense[0]}, {', '.join(expense[1])}\n")

    def load_expenses(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(', ')
                    amount = float(parts[0])
                    names = parts[1].split(', ')
                    self.expenses.append((amount, names))

    def save_shares(self) -> None:
        with open('shares.txt', 'w') as file:
            for name, share in self.shares.items():
                file.write(f"{name}: {share}\n")

    def load_shares(self) -> None:
        if os.path.exists('shares.txt'):
            with open('shares.txt', 'r') as file:
                for line in file:
                    name, share = line.strip().split(': ')
                    self.shares[name] = float(share)

class GUI:
    def __init__(self, splitter: ExpenseSplitter):
        self.splitter = splitter
        self.root = tk.Tk()
        self.root.title("Expense Splitter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.amount_label = tk.Label(self.root, text="Total Expense:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.names_label = tk.Label(self.root, text="Names (comma separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(self.root)
        self.names_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.pack()

        self.shares_display = tk.Text(self.root, height=10, width=50)
        self.shares_display.pack()

        self.root.mainloop()

    def submit_expense(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            names = [name.strip() for name in self.names_entry.get().split(',')]
            if not names or amount <= 0:
                raise ValueError("Invalid input")
            self.splitter.add_expense(amount, names)
            shares = self.splitter.calculate_shares()
            self.display_shares(shares)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def display_shares(self, shares: dict) -> None:
        self.shares_display.delete(1.0, tk.END)
        for name, share in shares.items():
            self.shares_display.insert(tk.END, f"{name}: {share:.2f}\n")

if __name__ == "__main__":
    splitter = ExpenseSplitter()
    app = GUI(splitter)