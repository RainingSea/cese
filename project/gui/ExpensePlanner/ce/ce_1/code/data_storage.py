import os

class DataStorage:
    def __init__(self):
        self.expenses_file = 'expenses.txt'
        self.budget_file = 'budget.txt'

    def save_expenses(self, expenses):
        with open(self.expenses_file, 'w') as file:
            for expense in expenses:
                file.write(f"{expense.amount}|{expense.category}\n")

    def save_budget(self, budget):
        with open(self.budget_file, 'w') as file:
            file.write(f"{budget}\n")

    def load_expenses(self):
        if os.path.exists(self.expenses_file):
            with open(self.expenses_file, 'r') as file:
                for line in file:
                    amount, category = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), category))

    def load_budget(self):
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as file:
                return float(file.readline().strip())
        return 0.0