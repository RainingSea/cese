import matplotlib.pyplot as plt
from typing import List
from expense_manager import Expense

class Visualization:
    def generate_chart(self, expenses: List[Expense]) -> None:
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
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()