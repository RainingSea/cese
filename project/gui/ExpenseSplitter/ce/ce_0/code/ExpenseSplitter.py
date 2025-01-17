import os
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
        total_amount = sum(expense.amount for expense in self.expenses)
        total_participants = sum(len(expense.participants) for expense in self.expenses)
        shares = {}
        if total_participants > 0:
            share_amount = total_amount / total_participants
            for expense in self.expenses:
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
                    amount, names = line.strip().split('|')
                    names_list = names.split(',')
                    self.add_expense(float(amount), names_list)

    def save_data(self):
        with open('expenses.txt', 'a') as file:
            for expense in self.expenses:
                names_str = ','.join(expense.participants)
                file.write(f"{expense.amount}|{names_str}\n")
        with open('participants.txt', 'w') as file:
            for participant in self.participants:
                file.write(f"{participant}\n")