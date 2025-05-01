import tkinter as tk
from tkinter import messagebox
from expense_manager import ExpenseManager
from data_validation import validate_expense_input
from visualization import Visualization

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Comparator")
        self.expense_manager = ExpenseManager()
        self.visualization = Visualization()

        self.create_widgets()
        self.expense_manager.load_expenses()

    def create_widgets(self):
        self.amount_label = tk.Label(self.master, text="Amount:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(self.master)
        self.category_entry.grid(row=1, column=1)

        self.date_label = tk.Label(self.master, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0)
        self.date_entry = tk.Entry(self.master)
        self.date_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.compare_button = tk.Button(self.master, text="Generate Comparison", command=self.generate_comparison)
        self.compare_button.grid(row=4, column=0, columnspan=2)

        self.expenses_listbox = tk.Listbox(self.master)
        self.expenses_listbox.grid(row=5, column=0, columnspan=2)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if validate_expense_input(amount, category, date):
            expense = self.expense_manager.add_expense(amount, category, date)
            self.expenses_listbox.insert(tk.END, f"{expense.amount} | {expense.category} | {expense.date}")
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter valid expense details.")

    def generate_comparison(self):
        category = self.category_entry.get()
        expenses = self.expense_manager.get_expenses_by_category(category)
        if expenses:
            self.visualization.generate_bar_chart(expenses)
        else:
            messagebox.showinfo("No Data", "No expenses found for the selected category.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()