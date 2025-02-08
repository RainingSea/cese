import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from expense_splitter import ExpenseSplitter

class GUI:
    def __init__(self, expense_splitter: ExpenseSplitter):
        self.expense_splitter = expense_splitter
        self.root = tk.Tk()
        self.root.title("Expense Splitter")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Total Expense:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Names (comma separated):").grid(row=1, column=0)
        self.names_entry = tk.Entry(self.root)
        self.names_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate Shares", command=self.calculate_and_display_shares)
        self.calculate_button.grid(row=2, columnspan=2)

        self.result_area = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.result_area.grid(row=3, columnspan=2)

        self.load_expenses()

    def calculate_and_display_shares(self):
        try:
            amount = float(self.amount_entry.get())
            names = self.names_entry.get().split(',')
            self.expense_splitter.add_expense(amount, [name.strip() for name in names])
            shares = self.expense_splitter.calculate_shares()
            self.result_area.delete(1.0, tk.END)
            for name, share in shares.items():
                self.result_area.insert(tk.END, f"{name}: {share:.2f}\n")
            self.expense_splitter.save_expenses()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def load_expenses(self):
        self.expense_splitter.load_expenses()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    expense_splitter = ExpenseSplitter()
    gui = GUI(expense_splitter)
    gui.run()