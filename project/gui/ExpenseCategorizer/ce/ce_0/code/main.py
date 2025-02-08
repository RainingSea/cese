import tkinter as tk
from tkinter import ttk, messagebox
from expense_categorizer import ExpenseCategorizer

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.categorizer = ExpenseCategorizer()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Amount:").grid(column=0, row=0)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.grid(column=1, row=0)

        ttk.Label(self.root, text="Description:").grid(column=0, row=1)
        self.description_entry = ttk.Entry(self.root)
        self.description_entry.grid(column=1, row=1)

        ttk.Label(self.root, text="Category:").grid(column=0, row=2)
        self.category_combobox = ttk.Combobox(self.root, values=self.categorizer.custom_categories)
        self.category_combobox.grid(column=1, row=2)

        self.add_button = ttk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(column=0, row=3)

        self.summary_button = ttk.Button(self.root, text="View Summary", command=self.view_summary)
        self.summary_button.grid(column=1, row=3)

        self.expense_listbox = tk.Listbox(self.root)
        self.expense_listbox.grid(column=0, row=4, columnspan=2)

        self.load_expenses()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_combobox.get()
            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return

            self.categorizer.add_expense(amount, description, category)
            self.expense_listbox.insert(tk.END, f"{amount} - {description} ({category})")
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.category_combobox.set('')
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")

    def load_expenses(self):
        for expense in self.categorizer.expenses:
            self.expense_listbox.insert(tk.END, f"{expense.amount} - {expense.description} ({expense.category})")

    def view_summary(self):
        summary = self.categorizer.get_summary()
        summary_str = "\n".join([f"{category}: {amount}" for category, amount in summary.items()])
        messagebox.showinfo("Expense Summary", summary_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()