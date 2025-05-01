import tkinter as tk
from tkinter import messagebox
from expenses import ExpenseManager
from budget import BudgetManager
from report import ReportManager
from data_storage import load_data, save_data
import matplotlib.pyplot as plt

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expense_manager = ExpenseManager()
        self.budget_manager = BudgetManager()
        self.report_manager = ReportManager()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # UI components for entering expenses
        tk.Label(self.root, text="Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Description:").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Category:").grid(row=2, column=0)
        self.category_var = tk.StringVar(self.root)
        self.category_dropdown = tk.OptionMenu(self.root, self.category_var, *self.load_categories())
        self.category_dropdown.grid(row=2, column=1)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=3, columnspan=2)
        tk.Button(self.root, text="Generate Report", command=self.generate_report).grid(row=4, columnspan=2)
        tk.Button(self.root, text="Visualize Budget", command=self.visualize_budget).grid(row=5, columnspan=2)

    def load_data(self):
        self.expense_manager.load_expenses()
        budget_goal = load_data('budget_goals.txt')
        if budget_goal is not None:
            self.budget_manager.budget_goal = float(budget_goal)

    def load_categories(self):
        with open('categories.txt', 'r') as file:
            return [line.strip() for line in file.readlines()]

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get()
            self.expense_manager.add_expense(amount, category, description)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.track_budget()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def track_budget(self):
        remaining_budget = self.budget_manager.track_spending(self.expense_manager.expenses)
        messagebox.showinfo("Budget Status", f"Remaining Budget: {remaining_budget:.2f}")

    def generate_report(self):
        report = self.report_manager.generate_report(self.expense_manager.expenses)
        messagebox.showinfo("Report", report)

    def visualize_budget(self):
        categories = {}
        for expense in self.expense_manager.expenses:
            if expense.category in categories:
                categories[expense.category] += expense.amount
            else:
                categories[expense.category] = expense.amount

        plt.bar(categories.keys(), categories.values())
        plt.title('Budget Breakdown')
        plt.xlabel('Categories')
        plt.ylabel('Amount Spent')
        plt.show()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()