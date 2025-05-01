import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

class Investment:
    def __init__(self, name: str, amount: float, type: str):
        self.name = name
        self.amount = amount
        self.type = type

class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.investments = []

class Goal:
    def __init__(self, description: str, target_amount: float):
        self.description = description
        self.target_amount = target_amount

class InvestmentTracker:
    def __init__(self):
        self.investments = []
        self.portfolios = []
        self.goals = []
        self.load_data()

    def add_investment(self, investment: Investment):
        self.investments.append(investment)
        self.save_investments()

    def categorize_investment(self, investment: Investment, portfolio: Portfolio):
        portfolio.investments.append(investment)
        self.save_portfolios()

    def generate_visualization(self):
        amounts = [inv.amount for inv in self.investments]
        names = [inv.name for inv in self.investments]
        plt.bar(names, amounts)
        plt.xlabel('Investments')
        plt.ylabel('Amount')
        plt.title('Investment Visualization')
        plt.show()

    def generate_report(self):
        report = "Investment Report:\n"
        for inv in self.investments:
            report += f"{inv.name}: ${inv.amount} ({inv.type})\n"
        messagebox.showinfo("Investment Report", report)

    def set_goal(self, goal: Goal):
        self.goals.append(goal)
        self.save_goals()

    def load_data(self):
        self.load_investments()
        self.load_portfolios()
        self.load_goals()

    def load_investments(self):
        try:
            with open('investments.txt', 'r') as f:
                for line in f:
                    name, amount, type_ = line.strip().split('|')
                    self.add_investment(Investment(name, float(amount), type_))
        except FileNotFoundError:
            pass

    def load_portfolios(self):
        try:
            with open('portfolios.txt', 'r') as f:
                for line in f:
                    name = line.strip()
                    self.portfolios.append(Portfolio(name))
        except FileNotFoundError:
            pass

    def load_goals(self):
        try:
            with open('goals.txt', 'r') as f:
                for line in f:
                    description, target_amount = line.strip().split('|')
                    self.set_goal(Goal(description, float(target_amount)))
        except FileNotFoundError:
            pass

    def save_investments(self):
        with open('investments.txt', 'w') as f:
            for inv in self.investments:
                f.write(f"{inv.name}|{inv.amount}|{inv.type}\n")

    def save_portfolios(self):
        with open('portfolios.txt', 'w') as f:
            for portfolio in self.portfolios:
                f.write(f"{portfolio.name}\n")

    def save_goals(self):
        with open('goals.txt', 'w') as f:
            for goal in self.goals:
                f.write(f"{goal.description}|{goal.target_amount}\n")

class InvestmentApp:
    def __init__(self, master):
        self.master = master
        self.tracker = InvestmentTracker()
        self.master.title("Investment Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.investment_name = tk.Entry(self.master)
        self.investment_name.pack()
        self.investment_amount = tk.Entry(self.master)
        self.investment_amount.pack()
        self.investment_type = tk.Entry(self.master)
        self.investment_type.pack()

        self.add_button = tk.Button(self.master, text="Add Investment", command=self.add_investment)
        self.add_button.pack()

        self.visualize_button = tk.Button(self.master, text="Generate Visualization", command=self.tracker.generate_visualization)
        self.visualize_button.pack()

        self.report_button = tk.Button(self.master, text="Generate Report", command=self.tracker.generate_report)
        self.report_button.pack()

    def add_investment(self):
        name = self.investment_name.get()
        amount = float(self.investment_amount.get())
        type_ = self.investment_type.get()
        self.tracker.add_investment(Investment(name, amount, type_))
        messagebox.showinfo("Success", "Investment added successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()