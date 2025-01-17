import tkinter as tk
from tkinter import messagebox
from expenses import ExpenseComparator

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expense_comparator = ExpenseComparator()
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=3, columnspan=2)

        tk.Button(self.root, text="Generate Chart", command=self.generate_chart).grid(row=4, columnspan=2)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        self.expense_comparator.add_expense(date, category, amount)
        messagebox.showinfo("Success", "Expense added successfully!")

    def generate_chart(self):
        start_date = self.date_entry.get()
        end_date = self.category_entry.get()
        data = self.expense_comparator.compare_expenses(start_date, end_date)
        if data:
            self.expense_comparator.generate_chart(data)
        else:
            messagebox.showwarning("No Data", "No expenses found for the given date range.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()