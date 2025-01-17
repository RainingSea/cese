import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter")
        self.splitter = ExpenseSplitter()

        self.amount_label = tk.Label(root, text="Total Expense Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.names_label = tk.Label(root, text="Names of Individuals (comma separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(root)
        self.names_entry.pack()

        self.submit_button = tk.Button(root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.pack()

        self.result_area = tk.Text(root, height=10, width=50)
        self.result_area.pack()

    def submit_expense(self):
        try:
            amount = float(self.amount_entry.get())
            names = self.names_entry.get().split(',')
            names = [name.strip() for name in names if name.strip()]
            self.splitter.add_expense(amount, names)
            shares = self.splitter.calculate_shares()
            self.display_shares(shares)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def display_shares(self, shares):
        self.result_area.delete(1.0, tk.END)
        for participant, share in shares.items():
            self.result_area.insert(tk.END, f"{participant}: ${share:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()