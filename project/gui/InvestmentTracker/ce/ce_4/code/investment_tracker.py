from investment import Investment
from file_handler import write_investment, read_investments, write_report

class InvestmentTracker:
    def __init__(self):
        self.investments = read_investments()

    def add_investment(self, name: str, type: str, amount: float, date: str, category: str) -> None:
        investment = Investment(name, type, amount, date, category)
        self.investments.append(investment)
        write_investment(investment)

    def generate_report(self) -> str:
        report = "Investment Report:\n"
        for investment in self.investments:
            report += f"Name: {investment.name}, Type: {investment.type}, Amount: {investment.amount}, Date: {investment.date}, Category: {investment.category}\n"
        write_report(report)
        return report

    def visualize_performance(self) -> None:
        # Visualization logic can be implemented here using matplotlib
        pass

    def set_investment_goals(self, goals: str) -> None:
        # Logic for setting investment goals can be implemented here
        pass