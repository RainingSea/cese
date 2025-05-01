import tkinter as tk
from tkinter import ttk
from expense_manager import ExpenseManager
from visualization import Visualization
from data_storage import load_expenses, load_categories

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Comparator")
        self.expense_manager = ExpenseManager()
        self.visualizer = Visualization()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.frame_input = ttk.Frame(self.master)
        self.frame_input.pack(pady=10)

        self.label_date = ttk.Label(self.frame_input, text="Date (YYYY-MM-DD):")
        self.label_date.grid(row=0, column=0)
        self.entry_date = ttk.Entry(self.frame_input)
        self.entry_date.grid(row=0, column=1)

        self.label_amount = ttk.Label(self.frame_input, text="Amount:")
        self.label_amount.grid(row=1, column=0)
        self.entry_amount = ttk.Entry(self.frame_input)
        self.entry_amount.grid(row=1, column=1)

        self.label_category = ttk.Label(self.frame_input, text="Category:")
        self.label_category.grid(row=2, column=0)
        self.combo_category = ttk.Combobox(self.frame_input)
        self.combo_category.grid(row=2, column=1)

        self.button_add = ttk.Button(self.frame_input, text="Add Expense", command=self.add_expense)
        self.button_add.grid(row=3, columnspan=2, pady=5)

        self.button_visualize = ttk.Button(self.frame_input, text="Generate Chart", command=self.generate_chart)
        self.button_visualize.grid(row=4, columnspan=2, pady=5)

        self.canvas = tk.Canvas(self.master, width=600, height=400)
        self.canvas.pack()

    def load_data(self):
        categories = load_categories()
        self.combo_category['values'] = categories

        expenses = load_expenses()
        for expense in expenses:
            self.expense_manager.add_expense(expense['date'], expense['amount'], expense['category'])

    def add_expense(self):
        date = self.entry_date.get()
        amount = float(self.entry_amount.get())
        category = self.combo_category.get()
        self.expense_manager.add_expense(date, amount, category)
        self.entry_date.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def generate_chart(self):
        expenses = self.expense_manager.get_expenses("2020-01-01", "2023-12-31")
        self.visualizer.generate_chart(expenses)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()