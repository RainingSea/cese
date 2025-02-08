import tkinter as tk
from tkinter import messagebox
from expense_planner import ExpensePlanner

class ExpensePlannerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Planner")
        self.planner = ExpensePlanner()
        self.planner.load_data()

        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.master, text="Amount:")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.pack()

        self.category_entry = tk.Entry(self.master)
        self.category_entry.pack()

        self.add_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.budget_label = tk.Label(self.master, text="Set Budget Goal:")
        self.budget_label.pack()

        self.budget_category_entry = tk.Entry(self.master)
        self.budget_category_entry.pack()

        self.budget_amount_entry = tk.Entry(self.master)
        self.budget_amount_entry.pack()

        self.set_budget_button = tk.Button(self.master, text="Set Budget", command=self.set_budget_goal)
        self.set_budget_button.pack()

        self.report_button = tk.Button(self.master, text="Generate Report", command=self.generate_report)
        self.report_button.pack()

        self.visualize_button = tk.Button(self.master, text="Visualize Budget", command=self.visualize_budget)
        self.visualize_button.pack()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            self.planner.add_expense(amount, category)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    def set_budget_goal(self):
        category = self.budget_category_entry.get()
        try:
            amount = float(self.budget_amount_entry.get())
            self.planner.set_budget_goal(category, amount)
            messagebox.showinfo("Success", "Budget goal set successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid budget amount entered.")

    def generate_report(self):
        report = self.planner.generate_report()
        messagebox.showinfo("Expense Report", report)

    def visualize_budget(self):
        self.planner.visualize_budget()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpensePlannerApp(root)
    root.mainloop()