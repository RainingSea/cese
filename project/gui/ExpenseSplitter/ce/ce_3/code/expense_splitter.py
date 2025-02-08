import os

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, amount: float, names: list):
        self.expenses.append((amount, names))

    def calculate_shares(self) -> dict:
        if not self.expenses:
            return {}
        last_expense = self.expenses[-1]
        amount, names = last_expense
        share = amount / len(names)
        return {name: share for name in names}

    def load_expenses(self):
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    amount = float(parts[0])
                    names = parts[1:]
                    self.expenses.append((amount, names))

    def save_expenses(self):
        with open('expenses.txt', 'w') as file:
            for amount, names in self.expenses:
                file.write(f"{amount},{','.join(names)}\n")