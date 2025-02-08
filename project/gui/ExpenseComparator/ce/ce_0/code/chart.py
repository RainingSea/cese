import matplotlib.pyplot as plt

def generate_expense_chart(data: dict) -> None:
    categories = list(data.keys())
    amounts = list(data.values())
    
    plt.bar(categories, amounts)
    plt.xlabel('Categories')
    plt.ylabel('Amount')
    plt.title('Expense Comparison')
    plt.show()