import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from expense_manager import Expense, ExpenseManager
from visualization import generate_expense_chart

class ExpenseComparatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Comparator")
        self.expense_manager = ExpenseManager()
        self.expense_manager.load_expenses('expenses.txt')
        
        self.create_widgets()

    def create_widgets(self):
        self.date_label = ttk.Label(self.master, text="Date (YYYY-MM-DD):")
        self.date_label.grid(column=0, row=0)
        self.date_entry = ttk.Entry(self.master)
        self.date_entry.grid(column=1, row=0)

        self.category_label = ttk.Label(self.master, text="Category:")
        self.category_label.grid(column=0, row=1)
        self.category_entry = ttk.Entry(self.master)
        self.category_entry.grid(column=1, row=1)

        self.amount_label = ttk.Label(self.master, text="Amount:")
        self.amount_label.grid(column=0, row=2)
        self.amount_entry = ttk.Entry(self.master)
        self.amount_entry.grid(column=1, row=2)

        self.submit_button = ttk.Button(self.master, text="Submit Expense", command=self.submit_expense)
        self.submit_button.grid(column=0, row=3, columnspan=2)

        self.report_button = ttk.Button(self.master, text="Generate Report", command=self.generate_report)
        self.report_button.grid(column=0, row=4, columnspan=2)

    def submit_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        
        expense = Expense(date, category, amount)
        self.expense_manager.add_expense(expense)
        self.expense_manager.save_expenses('expenses.txt')
        messagebox.showinfo("Success", "Expense added successfully!")

    def generate_report(self):
        generate_expense_chart(self.expense_manager.expenses)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseComparatorApp(root)
    app.run()