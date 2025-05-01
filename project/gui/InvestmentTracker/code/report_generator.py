import matplotlib.pyplot as plt

class ReportGenerator:
    def __init__(self, investment_manager):
        self.investment_manager = investment_manager

    def generate_report(self) -> str:
        report = "Investment Report:\n"
        report += "===================\n"
        for investment in self.investment_manager.investments:
            report += f"Name: {investment.name}, Type: {investment.type}, Amount: {investment.amount}, Date: {investment.date}\n"
        return report

    def visualize_performance(self):
        amounts = [investment.amount for investment in self.investment_manager.investments]
        names = [investment.name for investment in self.investment_manager.investments]
        plt.bar(names, amounts)
        plt.xlabel('Investment Names')
        plt.ylabel('Investment Amounts')
        plt.title('Investment Performance')
        plt.show()