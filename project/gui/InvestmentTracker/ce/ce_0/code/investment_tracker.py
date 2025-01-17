import json
import os

class Investment:
    def __init__(self, id: int, type: str, amount: float, date: str, category: str):
        self.id = id
        self.type = type
        self.amount = amount
        self.date = date
        self.category = category

class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.investments = []

    def add_investment(self, investment: Investment) -> None:
        self.investments.append(investment)

class Goal:
    def __init__(self, description: str):
        self.description = description

class InvestmentTracker:
    def __init__(self):
        self.investments = []
        self.portfolios = []
        self.goals = []

    def add_investment(self, investment: dict) -> None:
        new_investment = Investment(**investment)
        self.investments.append(new_investment)
        self.save_data()

    def categorize_investment(self, investment_id: int, category: str) -> None:
        for investment in self.investments:
            if investment.id == investment_id:
                investment.category = category
                self.save_data()
                break

    def generate_report(self) -> str:
        report = "Investment Report:\n"
        for investment in self.investments:
            report += f"ID: {investment.id}, Type: {investment.type}, Amount: {investment.amount}, Date: {investment.date}, Category: {investment.category}\n"
        return report

    def set_goal(self, goal: str) -> None:
        new_goal = Goal(goal)
        self.goals.append(new_goal)
        self.save_data()

    def load_data(self) -> None:
        if os.path.exists('investments.txt'):
            with open('investments.txt', 'r') as file:
                for line in file:
                    id, type, amount, date, category = line.strip().split('|')
                    investment = Investment(int(id), type, float(amount), date, category)
                    self.investments.append(investment)

    def save_data(self) -> None:
        with open('investments.txt', 'w') as file:
            for investment in self.investments:
                file.write(f"{investment.id}|{investment.type}|{investment.amount}|{investment.date}|{investment.category}\n")