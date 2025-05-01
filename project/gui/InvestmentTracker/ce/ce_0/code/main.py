import tkinter as tk
from tkinter import ttk
from InvestmentTracker import InvestmentTracker
from data_management import load_investments, load_categories
from visualization import plot_investment_performance
from report_generation import generate_report

class InvestmentTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Tracker")
        
        self.tracker = InvestmentTracker()
        self.tracker.investments = load_investments()
        self.tracker.categories = load_categories()
        
        self.create_widgets()

    def create_widgets(self):
        # Input fields for investment details
        ttk.Label(self.root, text="Investment Name:").grid(column=0, row=0)
        self.investment_name = ttk.Entry(self.root)
        self.investment_name.grid(column=1, row=0)

        ttk.Label(self.root, text="Investment Type:").grid(column=0, row=1)
        self.investment_type = ttk.Entry(self.root)
        self.investment_type.grid(column=1, row=1)

        ttk.Label(self.root, text="Investment Amount:").grid(column=0, row=2)
        self.investment_amount = ttk.Entry(self.root)
        self.investment_amount.grid(column=1, row=2)

        ttk.Label(self.root, text="Investment Date:").grid(column=0, row=3)
        self.investment_date = ttk.Entry(self.root)
        self.investment_date.grid(column=1, row=3)

        # Dropdown menu for categories
        ttk.Label(self.root, text="Select Category:").grid(column=0, row=4)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_menu['values'] = [category.name for category in self.tracker.categories]
        self.category_menu.grid(column=1, row=4)

        # Button to add investment
        self.add_button = ttk.Button(self.root, text="Add Investment", command=self.add_investment)
        self.add_button.grid(column=0, row=5)

        # Button to generate report
        self.report_button = ttk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.grid(column=1, row=5)

        # Area for visualizations
        self.visualization_area = tk.Canvas(self.root, width=400, height=300)
        self.visualization_area.grid(column=0, row=6, columnspan=2)

    def add_investment(self):
        name = self.investment_name.get()
        type_ = self.investment_type.get()
        amount = float(self.investment_amount.get())
        date = self.investment_date.get()
        
        investment = Investment(name, type_, amount, date)
        self.tracker.add_investment(investment)
        self.tracker.categorize_investment(investment, self.category_var.get())
        self.plot_performance()

    def plot_performance(self):
        plot_investment_performance(self.tracker.investments, self.visualization_area)

    def generate_report(self):
        report = generate_report(self.tracker)
        print(report)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentTrackerApp(root)
    root.mainloop()