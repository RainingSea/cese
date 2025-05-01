import tkinter as tk
from tkinter import messagebox
import json
import os

class Expense:
    def __init__(self, total: float, names: list):
        self.total = total
        self.names = names

    def get_shares(self):
        if not self.names:
            return {}
        share = self.total / len(self.names)
        return {name: share for name in self.names}

class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, total: float, names: list):
        expense = Expense(total, names)
        self.expenses.append(expense)
        self.save_expenses()

    def calculate_shares(self):
        shares = {}
        for expense in self.expenses:
            shares.update(expense.get_shares())
        return shares

    def load_expenses(self):
        if os.path.exists('expenses.json'):
            with open('expenses.json', 'r') as file:
                data = json.load(file)
                for entry in data:
                    total = entry['total']
                    names = entry['names']
                    self.expenses.append(Expense(total, names))

    def save_expenses(self):
        data = [{'total': expense.total, 'names': expense.names} for expense in self.expenses]
        with open('expenses.json', 'w') as file:
            json.dump(data, file)

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Splitter")
        self.expense_manager = ExpenseManager()
        self.create_widgets()

    def create_widgets(self):
        self.total_label = tk.Label(self.master, text="Total Expense:")
        self.total_label.pack()

        self.total_entry = tk.Entry(self.master)
        self.total_entry.pack()

        self.names_label = tk.Label(self.master, text="Names (comma separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(self.master)
        self.names_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_expense)
        self.submit_button.pack()

        self.shares_button = tk.Button(self.master, text="Calculate Shares", command=self.display_shares)
        self.shares_button.pack()

        self.shares_display = tk.Text(self.master, height=10, width=50)
        self.shares_display.pack()

    def submit_expense(self):
        try:
            total = float(self.total_entry.get())
            names = [name.strip() for name in self.names_entry.get().split(',')]
            self.expense_manager.add_expense(total, names)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.total_entry.delete(0, tk.END)
            self.names_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid total amount.")

    def display_shares(self):
        shares = self.expense_manager.calculate_shares()
        self.shares_display.delete(1.0, tk.END)
        for name, share in shares.items():
            self.shares_display.insert(tk.END, f"{name}: {share:.2f}\n")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()