import matplotlib.pyplot as plt
from expense_manager import ExpensePlanner

def visualize_budget_breakdown(expense_planner: ExpensePlanner):
    categories = {}
    for expense in expense_planner.expenses:
        if expense.category in categories:
            categories[expense.category] += expense.amount
        else:
            categories[expense.category] = expense.amount

    plt.figure(figsize=(10, 6))
    plt.bar(categories.keys(), categories.values(), color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Amount Spent')
    plt.title('Budget Breakdown')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()