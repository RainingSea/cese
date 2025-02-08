import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class ExpenseSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter")
        self.splitter = ExpenseSplitter()

        self.amount_label = tk.Label(root, text="Total Expense Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.names_label = tk.Label(root, text="Names (comma separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(root)
        self.names_entry.pack()

        self.calculate_button = tk.Button(root, text="Calculate Shares", command=self.calculate_shares)
        self.calculate_button.pack()

        self.result_label = tk.Label(root, text="")
        self.result_label.pack()

    def calculate_shares(self):
        amount = float(self.amount_entry.get())
        names = self.names_entry.get().split(',')
        self.splitter.add_expense(amount, names)
        shares = self.splitter.calculate_shares()
        result = ", ".join([f"{name}: {shares[name]:.2f}" for name in shares])
        self.result_label.config(text=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSplitterApp(root)
    root.mainloop()