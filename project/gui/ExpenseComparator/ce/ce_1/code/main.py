import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from datetime import datetime
from expense_manager import ExpenseManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Comparator")
        self.expense_manager = ExpenseManager()
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        self.date_label = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0)
        self.category_combo = ttk.Combobox(self.root, values=self.expense_manager.categories)
        self.category_combo.grid(row=2, column=1)

        self.submit_button = tk.Button(self.root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.grid(row=3, column=0, columnspan=2)

        self.compare_button = tk.Button(self.root, text="Generate Comparison Report", command=self.generate_report)
        self.compare_button.grid(row=4, column=0, columnspan=2)

    def submit_expense(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combo.get()
        try:
            amount = float(amount)
            self.expense_manager.add_expense(date, amount, category)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")

    def generate_report(self):
        # Placeholder for report generation logic
        self.expense_manager.visualize_expenses()

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()