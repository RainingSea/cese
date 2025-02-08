import json
from datetime import datetime

class Expense:
    def __init__(self, date: str, category: str, amount: float):
        self.date = date
        self.category = category
        self.amount = amount

class ExpenseComparator:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def add_expense(self, date: str, category: str, amount: float):
        expense = Expense(date, category, amount)
        self.expenses.append(expense)
        self.save_expenses()

    def compare_expenses(self, start_date: str, end_date: str) -> dict:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        comparison = {}
        
        for expense in self.expenses:
            expense_date = datetime.strptime(expense.date, '%Y-%m-%d')
            if start_date <= expense_date <= end_date:
                if expense.category not in comparison:
                    comparison[expense.category] = 0
                comparison[expense.category] += expense.amount
        
        return comparison

    def generate_chart(self, data: dict) -> None:
        import matplotlib.pyplot as plt
        
        categories = list(data.keys())
        amounts = list(data.values())
        
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.title('Expense Comparison')
        plt.show()

    def load_expenses(self) -> None:
        try:
            with open('expenses.json', 'r') as file:
                data = json.load(file)
                for entry in data:
                    self.add_expense(entry['date'], entry['category'], entry['amount'])
        except FileNotFoundError:
            self.expenses = []

    def save_expenses(self) -> None:
        with open('expenses.json', 'w') as file:
            json.dump([{'date': exp.date, 'category': exp.category, 'amount': exp.amount} for exp in self.expenses], file)