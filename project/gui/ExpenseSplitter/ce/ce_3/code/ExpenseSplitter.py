import os

class ExpenseSplitter:
    def __init__(self):
        self.expenses = []
        self.load_data()

    def add_expense(self, total_amount: float, names: list):
        self.expenses.append((total_amount, names))
        self.save_data()

    def calculate_shares(self) -> dict:
        shares = {}
        total_expense = sum(expense[0] for expense in self.expenses)
        total_people = sum(len(expense[1]) for expense in self.expenses)

        if total_people == 0:
            return shares

        share_per_person = total_expense / total_people

        for expense in self.expenses:
            for name in expense[1]:
                if name in shares:
                    shares[name] += share_per_person
                else:
                    shares[name] = share_per_person

        return shares

    def save_data(self):
        with open('expenses.txt', 'w') as file:
            for total_amount, names in self.expenses:
                file.write(f"{total_amount};{','.join(names)}\n")

    def load_data(self):
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    total_amount, names = line.strip().split(';')
                    self.expenses.append((float(total_amount), names.split(',')))