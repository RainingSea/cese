import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from investment_tracker import InvestmentTracker

class InvestmentApp:
    def __init__(self, master):
        self.master = master
        self.tracker = InvestmentTracker()
        self.tracker.load_data()
        
        master.title("Investment Tracker")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Investment Tracker")
        self.label.pack()

        self.add_investment_button = tk.Button(self.master, text="Add Investment", command=self.add_investment)
        self.add_investment_button.pack()

        self.report_button = tk.Button(self.master, text="Generate Report", command=self.generate_report)
        self.report_button.pack()

        self.visualize_button = tk.Button(self.master, text="Visualize Investments", command=self.visualize_investments)
        self.visualize_button.pack()

    def add_investment(self):
        # Placeholder for adding investment logic
        investment_details = {
            'id': 1,  # This should be dynamically generated
            'type': 'Stocks',
            'amount': 1000.0,
            'date': '2023-10-01',
            'category': 'Equities'
        }
        self.tracker.add_investment(investment_details)
        messagebox.showinfo("Success", "Investment added successfully!")

    def generate_report(self):
        report = self.tracker.generate_report()
        messagebox.showinfo("Investment Report", report)

    def visualize_investments(self):
        # Placeholder for visualization logic
        plt.plot([1, 2, 3], [1, 4, 9])  # Dummy data
        plt.title("Investment Performance")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()