import json
from typing import List, Dict

class Expense:
    def __init__(self, amount: float, names: List[str]) -> None:
        self.amount = amount
        self.names = names

    def get_shares(self) -> Dict[str, float]:
        share = self.amount / len(self.names)
        return {name: share for name in self.names}

class ExpenseSplitter:
    def __init__(self) -> None:
        self.expenses = []

    def add_expense(self, amount: float, names: List[str]) -> None:
        expense = Expense(amount, names)
        self.expenses.append(expense)
        self.save_expenses()

    def calculate_shares(self, expense: Expense) -> Dict[str, float]:
        return expense.get_shares()

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, names = line.strip().split('|')
                    names_list = names.split(',')
                    self.add_expense(float(amount), names_list)
        except FileNotFoundError:
            pass

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                names_str = ','.join(expense.names)
                file.write(f"{expense.amount}|{names_str}\n")