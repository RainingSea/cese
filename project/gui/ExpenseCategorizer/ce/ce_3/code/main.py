import tkinter as tk
from tkinter import ttk
from ExpenseCategorizer import ExpenseCategorizer

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Categorizer")
        self.categorizer = ExpenseCategorizer()

        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack()

        self.category_combobox = ttk.Combobox(root, values=[category.name for category in self.categorizer.categories])
        self.category_combobox.pack()

        self.date_entry = tk.Entry(root)
        self.date_entry.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.pack()

        self.summary_button = tk.Button(root, text="Get Summary", command=self.show_summary)
        self.summary_button.pack()

        self.display_area = tk.Text(root)
        self.display_area.pack()

    def add_expense(self):
        amount = float(self.amount_entry.get())
        category = self.category_combobox.get()
        date = self.date_entry.get()
        self.categorizer.add_expense(amount, category, date)
        self.display_area.insert(tk.END, f"Added: {amount} to {category} on {date}\n")

    def show_summary(self):
        summary = self.categorizer.get_summary()
        self.display_area.insert(tk.END, "Summary:\n")
        for category, total in summary.items():
            self.display_area.insert(tk.END, f"{category}: {total}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()