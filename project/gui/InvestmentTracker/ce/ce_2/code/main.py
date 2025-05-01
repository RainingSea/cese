import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import datetime

class InvestmentTracker:
    def __init__(self):
        self.stocks = []
        self.bonds = []
        self.mutual_funds = []
        self.other_assets = []
        self.load_data()

    def load_data(self):
        self.stocks = self.load_investments('stocks.txt')
        self.bonds = self.load_investments('bonds.txt')
        self.mutual_funds = self.load_investments('mutual_funds.txt')
        self.other_assets = self.load_investments('other_assets.txt')

    def load_investments(self, filename):
        investments = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    type_, amount, category, date = line.strip().split(',')
                    investments.append({'type': type_, 'amount': float(amount), 'category': category, 'date': date})
        except FileNotFoundError:
            pass
        return investments

    def input_investment(self, type: str, amount: float, category: str):
        investment = {'type': type, 'amount': amount, 'category': category, 'date': datetime.datetime.now().strftime('%Y-%m-%d')}
        if type == 'stock':
            self.stocks.append(investment)
            self.save_investment('stocks.txt', investment)
        elif type == 'bond':
            self.bonds.append(investment)
            self.save_investment('bonds.txt', investment)
        elif type == 'mutual_fund':
            self.mutual_funds.append(investment)
            self.save_investment('mutual_funds.txt', investment)
        elif type == 'other_asset':
            self.other_assets.append(investment)
            self.save_investment('other_assets.txt', investment)

    def save_investment(self, filename, investment):
        with open(filename, 'a') as file:
            file.write(f"{investment['type']},{investment['amount']},{investment['category']},{investment['date']}\n")

    def categorize_investment(self, type: str, category: str):
        pass  # Placeholder for future implementation

    def generate_report(self) -> str:
        report = "Investment Report\n\n"
        report += "Stocks:\n"
        for stock in self.stocks:
            report += f"{stock['type']} | {stock['amount']} | {stock['category']} | {stock['date']}\n"
        report += "\nBonds:\n"
        for bond in self.bonds:
            report += f"{bond['type']} | {bond['amount']} | {bond['category']} | {bond['date']}\n"
        report += "\nMutual Funds:\n"
        for fund in self.mutual_funds:
            report += f"{fund['type']} | {fund['amount']} | {fund['category']} | {fund['date']}\n"
        report += "\nOther Assets:\n"
        for asset in self.other_assets:
            report += f"{asset['type']} | {asset['amount']} | {asset['category']} | {asset['date']}\n"
        return report

    def visualize_performance(self):
        types = ['Stocks', 'Bonds', 'Mutual Funds', 'Other Assets']
        amounts = [sum(investment['amount'] for investment in self.stocks),
                   sum(investment['amount'] for investment in self.bonds),
                   sum(investment['amount'] for investment in self.mutual_funds),
                   sum(investment['amount'] for investment in self.other_assets)]
        
        plt.bar(types, amounts)
        plt.xlabel('Investment Types')
        plt.ylabel('Total Amount')
        plt.title('Investment Performance')
        plt.show()

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Tracker")
        self.tracker = InvestmentTracker()
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        self.input_tab = ttk.Frame(tab_control)
        self.performance_tab = ttk.Frame(tab_control)
        self.report_tab = ttk.Frame(tab_control)

        tab_control.add(self.input_tab, text='Input Investments')
        tab_control.add(self.performance_tab, text='View Performance')
        tab_control.add(self.report_tab, text='Generate Reports')

        tab_control.pack(expand=1, fill='both')

        self.create_input_tab()
        self.create_performance_tab()
        self.create_report_tab()

    def create_input_tab(self):
        ttk.Label(self.input_tab, text="Investment Type:").grid(column=0, row=0)
        self.type_entry = ttk.Combobox(self.input_tab, values=["stock", "bond", "mutual_fund", "other_asset"])
        self.type_entry.grid(column=1, row=0)

        ttk.Label(self.input_tab, text="Amount:").grid(column=0, row=1)
        self.amount_entry = ttk.Entry(self.input_tab)
        self.amount_entry.grid(column=1, row=1)

        ttk.Label(self.input_tab, text="Category:").grid(column=0, row=2)
        self.category_entry = ttk.Entry(self.input_tab)
        self.category_entry.grid(column=1, row=2)

        self.submit_button = ttk.Button(self.input_tab, text="Submit", command=self.submit_investment)
        self.submit_button.grid(column=0, row=3, columnspan=2)

    def submit_investment(self):
        investment_type = self.type_entry.get()
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            self.tracker.input_investment(investment_type, amount, category)
            messagebox.showinfo("Success", "Investment added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def create_performance_tab(self):
        self.visualize_button = ttk.Button(self.performance_tab, text="Visualize Performance", command=self.tracker.visualize_performance)
        self.visualize_button.pack(pady=20)

    def create_report_tab(self):
        self.report_button = ttk.Button(self.report_tab, text="Generate Report", command=self.show_report)
        self.report_button.pack(pady=20)

    def show_report(self):
        report = self.tracker.generate_report()
        report_window = tk.Toplevel(self.root)
        report_window.title("Investment Report")
        report_text = tk.Text(report_window)
        report_text.insert(tk.END, report)
        report_text.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()