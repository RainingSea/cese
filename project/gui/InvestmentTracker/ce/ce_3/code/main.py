import tkinter as tk
from tkinter import messagebox
from investment_tracker import InvestmentTracker

class InvestmentApp:
    def __init__(self, root):
        self.tracker = InvestmentTracker()
        self.root = root
        self.root.title("Investment Tracker")

        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Investment Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.type_label = tk.Label(self.root, text="Investment Type:")
        self.type_label.pack()
        self.type_entry = tk.Entry(self.root)
        self.type_entry.pack()

        self.amount_label = tk.Label(self.root, text="Investment Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.date_label = tk.Label(self.root, text="Investment Date:")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Investment", command=self.add_investment)
        self.add_button.pack()

        self.visualize_button = tk.Button(self.root, text="Visualize Performance", command=self.visualize_performance)
        self.visualize_button.pack()

        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.pack()

    def add_investment(self):
        name = self.name_entry.get()
        type = self.type_entry.get()
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        self.tracker.add_investment(name, type, amount, date)
        messagebox.showinfo("Success", "Investment added successfully!")

    def visualize_performance(self):
        self.tracker.visualize_performance()

    def generate_report(self):
        report = self.tracker.generate_report()
        messagebox.showinfo("Investment Report", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()