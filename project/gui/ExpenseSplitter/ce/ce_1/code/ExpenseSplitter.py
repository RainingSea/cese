import json
from Expense import Expense

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.participants = []
        self.load_data()

    def add_expense(self, amount: float, names: list):
        expense = Expense(amount, names)
        self.expenses.append(expense)
        self.save_data()

    def calculate_shares(self) -> dict:
        total_shares = {}
        for expense in self.expenses:
            shares = expense.get_share()
            for participant, share in shares.items():
                if participant in total_shares:
                    total_shares[participant] += share
                else:
                    total_shares[participant] = share
        return total_shares

    def load_data(self):
        try:
            with open('expenses.txt', 'r') as f:
                for line in f:
                    amount, names = line.strip().split('|')
                    names_list = names.split(',')
                    self.add_expense(float(amount), names_list)
        except FileNotFoundError:
            pass

        try:
            with open('participants.txt', 'r') as f:
                self.participants = [line.strip() for line in f]
        except FileNotFoundError:
            pass

    def save_data(self):
        with open('expenses.txt', 'w') as f:
            for expense in self.expenses:
                names = ','.join(expense.participants)
                f.write(f"{expense.amount}|{names}\n")

        with open('participants.txt', 'w') as f:
            for participant in self.participants:
                f.write(f"{participant}\n")