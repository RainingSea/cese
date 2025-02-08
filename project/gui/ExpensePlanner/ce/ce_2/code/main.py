import tkinter as tk
from tkinter import ttk, messagebox
from ExpensePlanner import ExpensePlanner

class ExpenseApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Expense Planner")
        self.planner = ExpensePlanner()

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.description_label = tk.Label(root, text="Description:")
        self.description_label.grid(row=1, column=0)
        self.description_entry = tk.Entry(root)
        self.description_entry.grid(row=1, column=1)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=2, column=0)
        self.category_combobox = ttk.Combobox(root, values=list(self.planner.budget_goals.keys()))
        self.category_combobox.grid(row=2, column=1)

        self.submit_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=3, columnspan=2)

        self.report_button = tk.Button(root, text="Generate Report", command=self.show_report)
        self.report_button.grid(row=4, columnspan=2)

    def add_expense(self) -> None:
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_combobox.get()
            if category:
                self.planner.add_expense(amount, description, category)
                messagebox.showinfo("Success", "Expense added successfully!")
            else:
                messagebox.showwarning("Warning", "Please select a category.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")

    def show_report(self) -> None:
        report = self.planner.generate_report()
        messagebox.showinfo("Expense Report", report)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()