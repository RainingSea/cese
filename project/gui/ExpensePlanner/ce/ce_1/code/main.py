import tkinter as tk
from tkinter import messagebox
from expense_manager import ExpensePlanner
from visualization import visualize_budget_breakdown
from report_generator import generate_report

class ExpensePlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Planner")
        self.expense_planner = ExpensePlanner()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category:").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Date:").grid(row=2, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1)

        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=3, columnspan=2)
        tk.Button(self.root, text="Set Budget Goal", command=self.set_budget_goal).grid(row=4, columnspan=2)
        tk.Button(self.root, text="Generate Report", command=self.show_report).grid(row=5, columnspan=2)
        tk.Button(self.root, text="Visualize Budget", command=self.visualize_budget).grid(row=6, columnspan=2)

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_entry.get()
        date = self.date_entry.get()
        self.expense_planner.add_expense(amount, category, date)
        messagebox.showinfo("Success", "Expense added successfully!")

    def set_budget_goal(self):
        category = self.category_entry.get()
        amount = float(self.amount_entry.get())
        self.expense_planner.set_budget_goal(category, amount)
        messagebox.showinfo("Success", "Budget goal set successfully!")

    def show_report(self):
        report = generate_report(self.expense_planner)
        messagebox.showinfo("Report", report)

    def visualize_budget(self):
        visualize_budget_breakdown(self.expense_planner)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpensePlannerApp(root)
    root.mainloop()