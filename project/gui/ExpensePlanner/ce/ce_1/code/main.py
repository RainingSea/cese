import tkinter as tk
from tkinter import ttk
from expense_manager import ExpenseManager
from budget_manager import BudgetManager
from data_storage import DataStorage
from report_generator import ReportGenerator

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Planner")
        
        self.expense_manager = ExpenseManager()
        self.budget_manager = BudgetManager()
        self.data_storage = DataStorage()
        self.report_generator = ReportGenerator(self.expense_manager, self.budget_manager)

        self.setup_ui()

    def setup_ui(self):
        # Input field for expenses
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        # Dropdown for categories
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.root, textvariable=self.category_var)
        self.category_dropdown['values'] = ('Food', 'Transport', 'Utilities', 'Entertainment')
        self.category_dropdown.grid(row=0, column=2)

        # Button to add expense
        self.add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=0, column=3)

        # Budget input
        self.budget_entry = tk.Entry(self.root)
        self.budget_entry.grid(row=1, column=1)

        # Button to set budget
        self.set_budget_button = tk.Button(self.root, text="Set Budget", command=self.set_budget)
        self.set_budget_button.grid(row=1, column=2)

        # Button to generate report
        self.report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=2, column=1)

        # Display area for reports
        self.report_area = tk.Text(self.root, height=10, width=50)
        self.report_area.grid(row=3, column=1, columnspan=3)

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_var.get()
        self.expense_manager.add_expense(amount, category)
        self.data_storage.save_expenses(self.expense_manager.get_expenses())

    def set_budget(self):
        goal = float(self.budget_entry.get())
        self.budget_manager.set_budget(goal)
        self.data_storage.save_budget(goal)

    def generate_report(self):
        report = self.report_generator.generate_report()
        self.report_area.delete(1.0, tk.END)
        self.report_area.insert(tk.END, report)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()