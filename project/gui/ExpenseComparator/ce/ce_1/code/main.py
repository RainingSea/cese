import tkinter as tk
from tkinter import messagebox
from ExpenseComparator import ExpenseComparator

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Comparator")
        self.expense_comparator = ExpenseComparator()

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.pack()
        self.category_entry = tk.Entry(root)
        self.category_entry.pack()

        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.submit_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.submit_button.pack()

        self.compare_button = tk.Button(root, text="Compare Expenses", command=self.compare_expenses)
        self.compare_button.pack()

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get()
        self.expense_comparator.add_expense(amount, category, date)
        messagebox.showinfo("Success", "Expense added successfully!")

    def compare_expenses(self):
        start_date = self.date_entry.get()
        end_date = self.date_entry.get()
        comparison = self.expense_comparator.compare_expenses(start_date, end_date)
        self.expense_comparator.visualize_expenses(comparison)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()