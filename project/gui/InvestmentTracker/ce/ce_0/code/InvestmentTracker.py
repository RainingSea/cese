from Investment import Investment
from Category import Category

class InvestmentTracker:
    def __init__(self):
        self.investments = []
        self.categories = []

    def add_investment(self, investment: Investment):
        self.investments.append(investment)

    def categorize_investment(self, investment: Investment, category_name: str):
        for category in self.categories:
            if category.name == category_name:
                category.investments.append(investment)

    def generate_report(self) -> str:
        report = "Investment Report:\n"
        for investment in self.investments:
            report += f"{investment.name}: {investment.amount} on {investment.date}\n"
        return report

    def set_investment_goal(self, goal: str):
        self.investment_goal = goal