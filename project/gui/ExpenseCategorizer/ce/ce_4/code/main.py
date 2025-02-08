import tkinter as tk
from tkinter import ttk, messagebox
from ExpenseCategorizer import ExpenseCategorizer

class ExpenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Categorizer")
        self.categorizer = ExpenseCategorizer()
        
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=0, column=0)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.grid(row=1, column=0)

        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=1, column=1)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=2, column=0)

        self.category_combobox = ttk.Combobox(self.root, values=self.categorizer.categories)
        self.category_combobox.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, columnspan=2)

        self.summary_button = tk.Button(self.root, text="Show Summary", command=self.show_summary)
        self.summary_button.grid(row=4, columnspan=2)

        self.expenses_list = tk.Listbox(self.root)
        self.expenses_list.grid(row=5, columnspan=2)

        self.load_expenses()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_combobox.get()
            if category:
                self.categorizer.add_expense(amount, description, category)
                self.expenses_list.insert(tk.END, f"{description}: ${amount} in {category}")
                self.amount_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                self.category_combobox.set('')
            else:
                messagebox.showwarning("Warning", "Please select a category.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def load_expenses(self):
        self.expenses_list.delete(0, tk.END)
        for expense in self.categorizer.expenses:
            self.expenses_list.insert(tk.END, f"{expense.description}: ${expense.amount} in {expense.category}")

    def show_summary(self):
        summary = self.categorizer.get_summary()
        summary_text = "\n".join(f"{cat}: ${amt}" for cat, amt in summary.items())
        messagebox.showinfo("Summary", summary_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()