import tkinter as tk
from investment_tracker import InvestmentTracker

class InvestmentApp:
    def __init__(self, root):
        self.tracker = InvestmentTracker()
        self.root = root
        self.root.title("Investment Tracker")
        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Investment Name").grid(row=0)
        tk.Label(self.root, text="Investment Type").grid(row=1)
        tk.Label(self.root, text="Amount").grid(row=2)
        tk.Label(self.root, text="Date").grid(row=3)
        tk.Label(self.root, text="Category").grid(row=4)

        self.name_entry = tk.Entry(self.root)
        self.type_entry = tk.Entry(self.root)
        self.amount_entry = tk.Entry(self.root)
        self.date_entry = tk.Entry(self.root)
        self.category_entry = tk.Entry(self.root)

        self.name_entry.grid(row=0, column=1)
        self.type_entry.grid(row=1, column=1)
        self.amount_entry.grid(row=2, column=1)
        self.date_entry.grid(row=3, column=1)
        self.category_entry.grid(row=4, column=1)

        tk.Button(self.root, text='Add Investment', command=self.add_investment).grid(row=5, column=1)

    def add_investment(self):
        name = self.name_entry.get()
        type = self.type_entry.get()
        amount = float(self.amount_entry.get())
        date = self.date_entry.get()
        category = self.category_entry.get()
        self.tracker.add_investment(name, type, amount, date, category)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()