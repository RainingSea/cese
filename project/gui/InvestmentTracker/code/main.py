import tkinter as tk
from tkinter import messagebox
from data_management import InvestmentManager
from report_generator import ReportGenerator
from user_settings import UserSettings
import matplotlib.pyplot as plt

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Tracker")
        self.investment_manager = InvestmentManager()
        self.report_generator = ReportGenerator(self.investment_manager)
        self.user_settings = UserSettings()
        self.setup_ui()

    def setup_ui(self):
        # Input fields
        tk.Label(self.root, text="Investment Name:").grid(row=0, column=0)
        self.investment_name = tk.Entry(self.root)
        self.investment_name.grid(row=0, column=1)

        tk.Label(self.root, text="Investment Type:").grid(row=1, column=0)
        self.investment_type = tk.Entry(self.root)
        self.investment_type.grid(row=1, column=1)

        tk.Label(self.root, text="Amount:").grid(row=2, column=0)
        self.investment_amount = tk.Entry(self.root)
        self.investment_amount.grid(row=2, column=1)

        tk.Label(self.root, text="Date:").grid(row=3, column=0)
        self.investment_date = tk.Entry(self.root)
        self.investment_date.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Investment", command=self.add_investment).grid(row=4, column=0, columnspan=2)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=5, column=0, columnspan=2)
        tk.Button(self.root, text="Visualize Performance", command=self.visualize_performance).grid(row=6, column=0, columnspan=2)

    def add_investment(self):
        name = self.investment_name.get()
        type_ = self.investment_type.get()
        try:
            amount = float(self.investment_amount.get())
            date = self.investment_date.get()
            self.investment_manager.add_investment(name, type_, amount, date)
            messagebox.showinfo("Success", "Investment added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def generate_report(self):
        report = self.report_generator.generate_report()
        messagebox.showinfo("Report", report)

    def visualize_performance(self):
        amounts = [investment.amount for investment in self.investment_manager.investments]
        names = [investment.name for investment in self.investment_manager.investments]
        plt.bar(names, amounts)
        plt.xlabel('Investment Names')
        plt.ylabel('Investment Amounts')
        plt.title('Investment Performance')
        plt.show()

    def set_investment_goals(self, description: str, target_amount: float):
        goal = Goal(description, target_amount)
        self.user_settings.goals.append(goal)
        self.user_settings.save_settings()

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()