import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class GUI:
    def __init__(self, splitter: ExpenseSplitter):
        self.splitter = splitter
        self.root = tk.Tk()
        self.root.title("Expense Splitter")
        self.create_widgets()

    def create_widgets(self):
        self.total_amount_label = tk.Label(self.root, text="Total Expense:")
        self.total_amount_label.pack()

        self.total_amount_entry = tk.Entry(self.root)
        self.total_amount_entry.pack()

        self.names_label = tk.Label(self.root, text="Names (comma-separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(self.root)
        self.names_entry.pack()

        self.add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.calculate_shares_button = tk.Button(self.root, text="Calculate Shares", command=self.calculate_shares)
        self.calculate_shares_button.pack()

        self.result_area = tk.Text(self.root, height=10, width=50)
        self.result_area.pack()

    def add_expense(self):
        try:
            total_amount = float(self.total_amount_entry.get())
            names = self.names_entry.get().split(',')
            self.splitter.add_expense(total_amount, [name.strip() for name in names])
            messagebox.showinfo("Success", "Expense added successfully!")
            self.total_amount_entry.delete(0, tk.END)
            self.names_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid total amount.")

    def calculate_shares(self):
        shares = self.splitter.calculate_shares()
        self.result_area.delete(1.0, tk.END)
        if shares:
            for name, share in shares.items():
                self.result_area.insert(tk.END, f"{name}: {share:.2f}\n")
        else:
            self.result_area.insert(tk.END, "No expenses recorded.")

    def run(self):
        self.root.mainloop()