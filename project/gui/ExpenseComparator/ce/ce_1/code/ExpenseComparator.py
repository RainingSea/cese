import csv
from datetime import datetime
from Expense import Expense
from Category import Category

class ExpenseComparator:
    def __init__(self):
        self.file_path_expenses = 'expenses.txt'
        self.file_path_categories = 'categories.txt'

    def add_expense(self, amount: float, category: str, date: str) -> None:
        with open(self.file_path_expenses, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([amount, category, date])

    def get_expenses(self) -> list:
        expenses = []
        with open(self.file_path_expenses, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    expense = Expense(float(row[0]), row[1], row[2])
                    expenses.append(expense)
        return expenses

    def compare_expenses(self, start_date: str, end_date: str) -> dict:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        comparison = {}
        expenses = self.get_expenses()

        for expense in expenses:
            expense_date = datetime.strptime(expense.date, '%Y-%m-%d')
            if start_date <= expense_date <= end_date:
                if expense.category in comparison:
                    comparison[expense.category] += expense.amount
                else:
                    comparison[expense.category] = expense.amount
        return comparison

    def visualize_expenses(self, data: dict) -> None:
        import matplotlib.pyplot as plt

        categories = list(data.keys())
        amounts = list(data.values())

        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Total Amount')
        plt.title('Expense Comparison')
        plt.show()