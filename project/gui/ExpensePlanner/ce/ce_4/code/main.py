import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from datetime import datetime
import os

class Expense:
    def __init__(self, amount: float, category: str, date: str):
        self.amount = amount
        self.category = category
        self.date = date

class ExpensePlanner:
    def __init__(self):
        self.expenses = []
        self.budget_goals = {}
        self.load_data()

    def add_expense(self, amount: float, category: str):
        date = datetime.now().strftime("%Y-%m-%d")
        expense = Expense(amount, category, date)
        self.expenses.append(expense)
        self.save_data()

    def set_budget(self, category: str, amount: float):
        self.budget_goals[category] = amount
        self.save_data()

    def generate_report(self) -> str:
        report = "Expense Report:\n"
        for expense in self.expenses:
            report += f"{expense.date} - {expense.category}: ${expense.amount:.2f}\n"
        return report

    def visualize_budget(self) -> None:
        categories = list(self.budget_goals.keys())
        amounts = [self.budget_goals[cat] for cat in categories]
        plt.bar(categories, amounts)
        plt.xlabel('Categories')
        plt.ylabel('Budget Amount')
        plt.title('Budget Visualization')
        plt.show()

    def load_data(self) -> None:
        if os.path.exists('expenses.txt'):
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, category, date = line.strip().split('|')
                    self.expenses.append(Expense(float(amount), category, date))
        if os.path.exists('budgets.txt'):
            with open('budgets.txt', 'r') as file:
                for line in file:
                    category, amount = line.strip().split('|')
                    self.budget_goals[category] = float(amount)

    def save_data(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense.amount}|{expense.category}|{expense.date}\n")
        with open('budgets.txt', 'w') as file:
            for category, amount in self.budget_goals.items():
                file.write(f"{category}|{amount}\n")

class ExpensePlannerApp:
    def __init__(self, root):
        self.planner = ExpensePlanner()
        self.root = root
        self.root.title("Expense Planner")
        
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()
        
        self.category_entry = ttk.Combobox(root, values=["Food", "Transport", "Entertainment"])
        self.category_entry.pack()

        self.add_expense_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack()

        self.budget_button = tk.Button(root, text="Set Budget", command=self.set_budget)
        self.budget_button.pack()

        self.report_button = tk.Button(root, text="Generate Report", command=self.show_report)
        self.report_button.pack()

        self.visualize_button = tk.Button(root, text="Visualize Budget", command=self.planner.visualize_budget)
        self.visualize_button.pack()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            self.planner.add_expense(amount, category)
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def set_budget(self):
        category = self.category_entry.get()
        try:
            amount = float(self.amount_entry.get())
            self.planner.set_budget(category, amount)
            messagebox.showinfo("Success", "Budget set successfully.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def show_report(self):
        report = self.planner.generate_report()
        messagebox.showinfo("Report", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpensePlannerApp(root)
    root.mainloop()