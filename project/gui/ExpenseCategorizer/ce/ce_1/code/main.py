import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ExpenseManager:
    def __init__(self):
        self.expenses = []
        self.categories = []
        self.load_expenses()
        self.load_categories()

    def add_expense(self, amount: float, description: str, category: str) -> None:
        self.expenses.append((amount, description, category))
        self.save_expenses()

    def load_expenses(self) -> None:
        try:
            with open('expenses.txt', 'r') as file:
                for line in file:
                    amount, description, category = line.strip().split('|')
                    self.expenses.append((float(amount), description, category))
        except FileNotFoundError:
            self.expenses = []

    def load_categories(self) -> None:
        try:
            with open('categories.txt', 'r') as file:
                self.categories = [line.strip() for line in file]
        except FileNotFoundError:
            self.categories = []

    def save_expenses(self) -> None:
        with open('expenses.txt', 'w') as file:
            for expense in self.expenses:
                file.write(f"{expense[0]}|{expense[1]}|{expense[2]}\n")

    def save_categories(self) -> None:
        with open('categories.txt', 'w') as file:
            for category in self.categories:
                file.write(f"{category}\n")

    def get_summary(self) -> dict:
        summary = {}
        for amount, description, category in self.expenses:
            if category in summary:
                summary[category] += amount
            else:
                summary[category] = amount
        return summary

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Categorizer")
        self.expense_manager = ExpenseManager()

        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.master, text="Amount:")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self.master, text="Description:")
        self.description_label.grid(row=1, column=0)
        self.description_entry = tk.Entry(self.master)
        self.description_entry.grid(row=1, column=1)

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.grid(row=2, column=0)
        self.category_combobox = ttk.Combobox(self.master, values=self.expense_manager.categories)
        self.category_combobox.grid(row=2, column=1)

        self.submit_button = tk.Button(self.master, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=3, columnspan=2)

        self.summary_button = tk.Button(self.master, text="Show Summary", command=self.show_summary)
        self.summary_button.grid(row=4, columnspan=2)

        self.expense_listbox = tk.Listbox(self.master)
        self.expense_listbox.grid(row=5, columnspan=2)

        self.load_expenses_to_listbox()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_combobox.get()
            if category == "":
                messagebox.showerror("Error", "Please select a category.")
                return
            self.expense_manager.add_expense(amount, description, category)
            self.load_expenses_to_listbox()
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.category_combobox.set('')
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def load_expenses_to_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for amount, description, category in self.expense_manager.expenses:
            self.expense_listbox.insert(tk.END, f"{amount} | {description} | {category}")

    def show_summary(self):
        summary = self.expense_manager.get_summary()
        summary_message = "\n".join([f"{category}: ${amount:.2f}" for category, amount in summary.items()])
        messagebox.showinfo("Expense Summary", summary_message)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()