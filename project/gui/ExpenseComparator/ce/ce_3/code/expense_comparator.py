import matplotlib.pyplot as plt
from typing import List
from expense import Expense

class ExpenseComparator:
    def __init__(self):
        self.expenses = []

    def add_expense(self, date: str, amount: float, category: str) -> None:
        expense = Expense(date, amount, category)
        self.expenses.append(expense)

    def compare_expenses(self, start_date: str, end_date: str) -> List[Expense]:
        filtered_expenses = [
            expense for expense in self.expenses
            if start_date <= expense.date <= end_date
        ]
        return filtered_expenses

    def visualize_expenses(self, expenses: List[Expense]) -> None:
        categories = {}
        for expense in expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Categories')
        plt.ylabel('Total Amount')
        plt.title('Expenses Comparison')
        plt.show()