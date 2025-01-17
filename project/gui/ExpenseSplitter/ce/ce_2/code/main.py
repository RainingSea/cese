import tkinter as tk
from tkinter import messagebox
from typing import List, Dict

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, total_amount: float, names: List[str]) -> None:
        self.expenses.append((total_amount, names))
        self.save_expenses()

    def calculate_shares(self) -> Dict[str, float]:
        shares = {}
        for total_amount, names in self.expenses:
            share_per_person = total_amount / len(names)
            for name in names:
                if name in shares:
                    shares[name] += share_per_person
                else:
                    shares[name] = share_per_person
        return shares

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    total_amount, names = line.strip().split(';')
                    self.expenses.append((float(total_amount), names.split(',')))
        except FileNotFoundError:
            pass

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for total_amount, names in self.expenses:
                file.write(f"{total_amount};{','.join(names)}\n")

class GUI:
    def __init__(self, expense_splitter: ExpenseSplitter):
        self.expense_splitter = expense_splitter
        self.root = tk.Tk()
        self.root.title("Expense Splitter")
        self.create_widgets()

    def create_widgets(self) -> None:
        tk.Label(self.root, text="Total Expense:").grid(row=0, column=0)
        self.total_expense_entry = tk.Entry(self.root)
        self.total_expense_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Names (comma separated):").grid(row=1, column=0)
        self.names_entry = tk.Entry(self.root)
        self.names_entry.grid(row=1, column=1)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit_expense)
        self.submit_button.grid(row=2, columnspan=2)

        self.shares_display = tk.Text(self.root, height=10, width=30)
        self.shares_display.grid(row=3, columnspan=2)

    def submit_expense(self) -> None:
        try:
            total_amount = float(self.total_expense_entry.get())
            names = self.names_entry.get().split(',')
            names = [name.strip() for name in names if name.strip()]
            self.expense_splitter.add_expense(total_amount, names)
            shares = self.expense_splitter.calculate_shares()
            self.display_shares(shares)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for total expense.")

    def display_shares(self, shares: Dict[str, float]) -> None:
        self.shares_display.delete(1.0, tk.END)
        for name, share in shares.items():
            self.shares_display.insert(tk.END, f"{name}: ${share:.2f}\n")

if __name__ == "__main__":
    expense_splitter = ExpenseSplitter()
    gui = GUI(expense_splitter)
    gui.root.mainloop()