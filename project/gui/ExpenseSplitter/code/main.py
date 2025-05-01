import tkinter as tk
from tkinter import messagebox
from expense import Expense
from expense_manager import ExpenseManager

class Main:
    def __init__(self):
        self.expense_manager = ExpenseManager()
        self.root = tk.Tk()
        self.root.title("Expense Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.root, text="Total Expense Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.names_label = tk.Label(self.root, text="Names (comma separated):")
        self.names_label.pack()
        self.names_entry = tk.Entry(self.root)
        self.names_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.pack()

        self.clear_button = tk.Button(self.root, text="Clear Inputs", command=self.clear_inputs)
        self.clear_button.pack()

        self.expenses_listbox = tk.Listbox(self.root)
        self.expenses_listbox.pack()

        self.shares_display = tk.Text(self.root, height=10, width=50)
        self.shares_display.pack()

        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.pack()

        self.display_expenses()
        self.display_shares()

    def main(self):
        self.root.mainloop()

    def submit_expense(self) -> None:
        try:
            total_amount = float(self.amount_entry.get().strip())
            names = self.names_entry.get().split(',')
            names = [name.strip() for name in names if name.strip()]
            if not names:
                raise ValueError("At least one name must be provided.")
            expense = Expense(total_amount, names)
            self.expense_manager.add_expense(expense)
            self.display_expenses()
            self.display_shares()
            self.clear_inputs()
        except ValueError as e:
            self.error_label.config(text=str(e))

    def display_expenses(self) -> None:
        self.expenses_listbox.delete(0, tk.END)
        for expense in self.expense_manager.expenses:
            share = expense.calculate_share()
            expense_display = f"Total: {expense.total_amount}, Names: {', '.join(expense.names)}, Share: {share:.2f}"
            self.expenses_listbox.insert(tk.END, expense_display)

    def display_shares(self) -> None:
        shares = self.expense_manager.calculate_shares()
        self.shares_display.delete(1.0, tk.END)
        for name, share in shares.items():
            self.shares_display.insert(tk.END, f"{name}: {share:.2f}\n")

    def clear_inputs(self) -> None:
        self.amount_entry.delete(0, tk.END)
        self.names_entry.delete(0, tk.END)
        self.error_label.config(text="")