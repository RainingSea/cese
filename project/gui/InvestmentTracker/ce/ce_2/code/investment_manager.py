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

    def add_investment(self, investment: Investment):
        self.investments.append(investment)
        self.save_investments()

    def load_investments(self):
        if os.path.exists('investments.txt'):
            with open('investments.txt', 'r') as file:
                for line in file:
                    name, type_, amount, date = line.strip().split('|')
                    self.investments.append(Investment(name, type_, float(amount), date))

    def save_investments(self):
        with open('investments.txt', 'w') as file:
            for investment in self.investments:
                file.write(f"{investment.name}|{investment.type}|{investment.amount}|{investment.date}\n")