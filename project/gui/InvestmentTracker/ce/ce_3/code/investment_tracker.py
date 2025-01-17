import json
from investment import Investment
import matplotlib.pyplot as plt

class InvestmentTracker:
    def __init__(self):
        self.investments = []
        self.goals = {}
        self.load_data()

    def add_investment(self, name: str, type: str, amount: float, date: str):
        investment = Investment(name, type, amount, date)
        self.investments.append(investment)
        self.save_data()

    def categorize_investment(self, name: str, category: str):
        for investment in self.investments:
            if investment.name == name:
                investment.type = category
                self.save_data()
                break

    def set_goal(self, goal: str):
        self.goals[goal] = False
        self.save_data()

    def visualize_performance(self):
        names = [investment.name for investment in self.investments]
        amounts = [investment.amount for investment in self.investments]
        plt.bar(names, amounts)
        plt.xlabel('Investment Name')
        plt.ylabel('Amount')
        plt.title('Investment Performance')
        plt.show()

    def generate_report(self) -> str:
        report_lines = ["Investment Report:"]
        for investment in self.investments:
            report_lines.append(f"{investment.name}: {investment.amount} on {investment.date}")
        return "\n".join(report_lines)

    def load_data(self):
        try:
            with open('investments.json', 'r') as file:
                data = json.load(file)
                self.investments = [Investment(**inv) for inv in data.get('investments', [])]
                self.goals = data.get('goals', {})
        except FileNotFoundError:
            self.investments = []
            self.goals = {}

    def save_data(self):
        data = {
            'investments': [vars(inv) for inv in self.investments],
            'goals': self.goals
        }
        with open('investments.json', 'w') as file:
            json.dump(data, file, indent=4)