import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class GUI:
    def __init__(self, splitter: ExpenseSplitter):
        self.splitter = splitter
        self.root = tk.Tk()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Expense Splitter")

        tk.Label(self.root, text="Total Expense:").grid(row=0, column=0)
        self.total_entry = tk.Entry(self.root)
        self.total_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Names (comma-separated):").grid(row=1, column=0)
        self.names_entry = tk.Entry(self.root)
        self.names_entry.grid(row=1, column=1)

        self.calculate_button = tk.Button(self.root, text="Calculate Shares", command=self.calculate_button_clicked)
        self.calculate_button.grid(row=2, column=0, columnspan=2)

        self.result_display = tk.Text(self.root, height=10, width=40)
        self.result_display.grid(row=3, column=0, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save Expenses", command=self.save_button_clicked)
        self.save_button.grid(row=4, column=0)

        self.load_button = tk.Button(self.root, text="Load Expenses", command=self.load_button_clicked)
        self.load_button.grid(row=4, column=1)

    def calculate_button_clicked(self):
        try:
            total = float(self.total_entry.get())
            names = [name.strip() for name in self.names_entry.get().split(',')]
            self.splitter.add_expense(total, names)
            shares = self.splitter.calculate_shares()
            result = "\n".join(f"{name}: {amount:.2f}" for name, amount in shares.items())
            self.result_display.delete(1.0, tk.END)
            self.result_display.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid total and names.")

    def save_button_clicked(self):
        self.splitter.save_expenses('expenses.txt')
        messagebox.showinfo("Save", "Expenses saved successfully.")

    def load_button_clicked(self):
        self.splitter.load_expenses('expenses.txt')
        messagebox.showinfo("Load", "Expenses loaded successfully.")