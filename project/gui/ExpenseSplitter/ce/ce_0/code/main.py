import tkinter as tk
from tkinter import messagebox

class Expense:
    def __init__(self, amount: float, names: list):
        self.amount = amount
        self.names = names

    def get_share(self) -> dict:
        share_amount = self.amount / len(self.names)
        return {name: share_amount for name in self.names}

class Main:
    def __init__(self):
        self.expenses = []
        self.load_data()
        self.create_ui()

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("Expense Splitter")

        tk.Label(self.root, text="Total Expense:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Names (comma separated):").grid(row=1, column=0)
        self.names_entry = tk.Entry(self.root)
        self.names_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate Shares", command=self.calculate_shares)
        self.calculate_button.grid(row=2, column=0, columnspan=2)

        self.result_display = tk.Text(self.root, height=10, width=50)
        self.result_display.grid(row=3, column=0, columnspan=2)

        self.root.mainloop()

    def add_expense(self, amount: float, names: list):
        expense = Expense(amount, names)
        self.expenses.append(expense)
        self.save_data()

    def calculate_shares(self):
        try:
            amount = float(self.amount_entry.get())
            names = self.names_entry.get().split(',')
            names = [name.strip() for name in names if name.strip()]
            if not names:
                raise ValueError("No names provided.")

            self.add_expense(amount, names)
            shares = self.expenses[-1].get_share()
            self.result_display.delete(1.0, tk.END)
            for name, share in shares.items():
                self.result_display.insert(tk.END, f"{name}: ${share:.2f}\n")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def load_data(self):
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount_str, names_str = line.strip().split(';')
                    amount = float(amount_str)
                    names = names_str.split(',')
                    self.add_expense(amount, names)
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("File Error", str(e))

    def save_data(self):
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                names_str = ','.join(expense.names)
                file.write(f"{expense.amount};{names_str}\n")

if __name__ == "__main__":
    Main()