import tkinter as tk
from tkinter import messagebox
from typing import List, Dict

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, amount: float, names: List[str]) -> None:
        self.expenses.append({"amount": amount, "names": names})
        self.save_expenses()

    def calculate_shares(self) -> Dict[str, float]:
        shares = {}
        for expense in self.expenses:
            amount = expense["amount"]
            names = expense["names"]
            share = amount / len(names)
            for name in names:
                if name in shares:
                    shares[name] += share
                else:
                    shares[name] = share
        return shares

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount_str, *names = line.strip().split(',')
                    amount = float(amount_str)
                    self.expenses.append({"amount": amount, "names": names})
        except FileNotFoundError:
            pass

    def save_expenses(self) -> None:
        with open('expenses.txt', 'a') as file:
            for expense in self.expenses:
                amount = expense["amount"]
                names = ','.join(expense["names"])
                file.write(f"{amount},{names}\n")

class GUI:
    def __init__(self, splitter: ExpenseSplitter):
        self.splitter = splitter
        self.root = tk.Tk()
        self.root.title("Expense Splitter")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.amount_label = tk.Label(self.root, text="Total Expense Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.names_label = tk.Label(self.root, text="Names (comma separated):")
        self.names_label.pack()

        self.names_entry = tk.Entry(self.root)
        self.names_entry.pack()

        self.calculate_button = tk.Button(self.root, text="Calculate Shares", command=self.calculate)
        self.calculate_button.pack()

        self.results_label = tk.Label(self.root, text="")
        self.results_label.pack()

        self.previous_expenses_label = tk.Label(self.root, text="Previous Expenses:")
        self.previous_expenses_label.pack()

        self.previous_expenses_text = tk.Text(self.root, height=10, width=50)
        self.previous_expenses_text.pack()
        self.load_previous_expenses()

    def calculate(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            names = self.names_entry.get().split(',')
            names = [name.strip() for name in names if name.strip()]
            self.splitter.add_expense(amount, names)
            shares = self.splitter.calculate_shares()
            self.display_results(shares)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid amount.")

    def display_results(self, results: Dict[str, float]) -> None:
        result_text = "Shares:\n"
        for name, share in results.items():
            result_text += f"{name}: ${share:.2f}\n"
        self.results_label.config(text=result_text)

    def load_previous_expenses(self) -> None:
        self.previous_expenses_text.delete(1.0, tk.END)
        for expense in self.splitter.expenses:
            amount = expense["amount"]
            names = ', '.join(expense["names"])
            self.previous_expenses_text.insert(tk.END, f"{amount}, {names}\n")

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    expense_splitter = ExpenseSplitter()
    gui = GUI(expense_splitter)
    gui.run()