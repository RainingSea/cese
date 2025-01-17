import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from expense_comparator import ExpenseComparator

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expense_comparator = ExpenseComparator()

        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1)

        self.submit_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=3, column=0, columnspan=2)

        self.visualize_button = tk.Button(self.root, text="Visualize Expenses", command=self.visualize_expenses)
        self.visualize_button.grid(row=4, column=0, columnspan=2)

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get()

        self.expense_comparator.add_expense(date, amount, category)
        messagebox.showinfo("Success", "Expense added successfully!")

    def visualize_expenses(self):
        start_date = "2023-01-01"  # Example start date
        end_date = "2023-12-31"  # Example end date
        expenses = self.expense_comparator.compare_expenses(start_date, end_date)
        self.expense_comparator.visualize_expenses(expenses)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()