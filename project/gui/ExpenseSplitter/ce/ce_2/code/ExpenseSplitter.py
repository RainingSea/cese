import os
from Expense import Expense

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.participants = []
        self.load_data()

    def add_expense(self, total_amount: float, names: list):
        expense = Expense(total_amount, names)
        self.expenses.append(expense)
        self.save_data()

    def calculate_shares(self) -> dict:
        shares = {}
        for expense in self.expenses:
            share_amount = expense.total_amount / len(expense.participants)
            for participant in expense.participants:
                if participant in shares:
                    shares[participant] += share_amount
                else:
                    shares[participant] = share_amount
        return shares

    def load_data(self):
        if os.path.exists('participants.txt'):
            with open('participants.txt', 'r') as file:
                self.participants = [line.strip() for line in file.readlines()]
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file.readlines():
                    data = line.strip().split(', ')
                    total_amount = float(data[0])
                    names = data[1:]
                    self.add_expense(total_amount, names)

    def save_data(self):
        with open('participants.txt', 'w') as file:
            for participant in self.participants:
                file.write(participant + '\n')
        with open('expenses.txt', 'a') as file:
            for expense in self.expenses:
                file.write(f"{expense.total_amount}, {', '.join(expense.participants)}\n")