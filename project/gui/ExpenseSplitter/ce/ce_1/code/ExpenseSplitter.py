import os
from typing import List, Tuple, Dict

class ExpenseSplitter:
    def __init__(self):
        self.expenses: List[Tuple[float, List[str]]] = []
        self.load_expenses()

    def add_expense(self, total: float, names: List[str]) -> None:
        self.expenses.append((total, names))
        self.save_expenses()

    def calculate_shares(self) -> Dict[str, float]:
        shares = {}
        for total, names in self.expenses:
            share = total / len(names)
            for name in names:
                shares[name.strip()] = shares.get(name.strip(), 0) + share
        return shares

    def load_expenses(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    total_amount = float(parts[0])
                    names = parts[1:]
                    self.expenses.append((total_amount, names))

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for total, names in self.expenses:
                file.write(f"{total},{','.join(names)}\n")