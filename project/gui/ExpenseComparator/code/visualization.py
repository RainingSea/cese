import matplotlib.pyplot as plt
from expense import Expense
from typing import List

class Visualization:
    def generate_bar_chart(self, expenses: List[Expense]):
        categories = {}
        for expense in expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Categories')
        plt.ylabel('Total Amount')
        plt.title('Expenses by Category')
        plt.show()

    def generate_pie_chart(self, expenses: List[Expense]):
        categories = {}
        for expense in expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title('Expenses Distribution')
        plt.show()