import matplotlib.pyplot as plt

def visualize_investments(investments):
    names = [investment.name for investment in investments]
    amounts = [investment.amount for investment in investments]

    plt.bar(names, amounts)
    plt.xlabel('Investment Name')
    plt.ylabel('Amount')
    plt.title('Investment Visualization')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()