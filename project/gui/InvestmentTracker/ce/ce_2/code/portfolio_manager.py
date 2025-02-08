import os

class Portfolio:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

class PortfolioManager:
    def __init__(self):
        self.portfolios = []

    def add_portfolio(self, portfolio: Portfolio):
        self.portfolios.append(portfolio)
        self.save_portfolios()

    def load_portfolios(self):
        if os.path.exists('portfolios.txt'):
            with open('portfolios.txt', 'r') as file:
                for line in file:
                    name, type_ = line.strip().split('|')
                    self.portfolios.append(Portfolio(name, type_))

    def save_portfolios(self):
        with open('portfolios.txt', 'w') as file:
            for portfolio in self.portfolios:
                file.write(f"{portfolio.name}|{portfolio.type}\n")