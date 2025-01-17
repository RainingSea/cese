import tkinter as tk
from tkinter import messagebox
from investment_manager import InvestmentManager
from portfolio_manager import PortfolioManager
from goal_manager import GoalManager
from visualization import visualize_investments
from report_generator import generate_report

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Tracker")
        
        self.investment_manager = InvestmentManager()
        self.portfolio_manager = PortfolioManager()
        self.goal_manager = GoalManager()
        
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Create input fields and buttons
        self.investment_name_entry = tk.Entry(self.root)
        self.investment_type_entry = tk.Entry(self.root)
        self.investment_amount_entry = tk.Entry(self.root)
        self.investment_date_entry = tk.Entry(self.root)

        self.add_investment_button = tk.Button(self.root, text="Add Investment", command=self.add_investment)
        self.visualize_button = tk.Button(self.root, text="Visualize Investments", command=self.visualize_investments)
        self.generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)

        # Layout
        self.investment_name_entry.pack()
        self.investment_type_entry.pack()
        self.investment_amount_entry.pack()
        self.investment_date_entry.pack()
        self.add_investment_button.pack()
        self.visualize_button.pack()
        self.generate_report_button.pack()

    def load_data(self):
        self.investment_manager.load_investments()
        self.portfolio_manager.load_portfolios()
        self.goal_manager.load_goals()

    def add_investment(self):
        name = self.investment_name_entry.get()
        type_ = self.investment_type_entry.get()
        amount = float(self.investment_amount_entry.get())
        date = self.investment_date_entry.get()
        investment = Investment(name, type_, amount, date)
        self.investment_manager.add_investment(investment)
        messagebox.showinfo("Success", "Investment added successfully!")

    def visualize_investments(self):
        visualize_investments(self.investment_manager.investments)

    def generate_report(self):
        report = generate_report(self.investment_manager.investments)
        messagebox.showinfo("Report", report)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()