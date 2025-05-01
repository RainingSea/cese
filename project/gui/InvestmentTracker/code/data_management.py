import os

class Investment:
    def __init__(self, name: str, type: str, amount: float, date: str):
        self.name = name
        self.type = type
        self.amount = amount
        self.date = date

class InvestmentManager:
    def __init__(self):
        self.investments = []
        self.load_investments()

    def add_investment(self, name: str, type: str, amount: float, date: str):
        investment = Investment(name, type, amount, date)
        self.investments.append(investment)
        self.save_investments()

    def edit_investment(self, index: int, name: str, type: str, amount: float, date: str):
        if 0 <= index < len(self.investments):
            self.investments[index] = Investment(name, type, amount, date)
            self.save_investments()

    def delete_investment(self, index: int):
        if 0 <= index < len(self.investments):
            del self.investments[index]
            self.save_investments()

    def load_investments(self):
        if os.path.exists('investments.txt'):
            with open('investments.txt', 'r') as file:
                for line in file:
                    name, type, amount, date = line.strip().split(',')
                    self.investments.append(Investment(name, type, float(amount), date))

    def save_investments(self):
        with open('investments.txt', 'w') as file:
            for investment in self.investments:
                file.write(f"{investment.name},{investment.type},{investment.amount},{investment.date}\n")

    def categorize_investments(self):
        categories = {}
        for investment in self.investments:
            if investment.type not in categories:
                categories[investment.type] = []
            categories[investment.type].append(investment)
        return categories