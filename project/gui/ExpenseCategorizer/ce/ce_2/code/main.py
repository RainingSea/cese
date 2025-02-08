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
        """Create and arrange UI components."""
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

        self.submit_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        self.submit_button.grid(row=3, columnspan=2)

        self.summary_button = tk.Button(self.root, text="View Summary", command=self.view_summary)
        self.summary_button.grid(row=4, columnspan=2)

    def add_expense(self):
        """Add an expense based on user input."""
        try:
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()
            category = self.category_combobox.get()
            if category not in self.categorizer.categories:
                self.categorizer.categories.append(category)
                self.categorizer.save_categories()
            self.categorizer.add_expense(amount, description, category)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def view_summary(self):
        """Display a summary of categorized expenses."""
        summary = self.categorizer.display_summary()
        messagebox.showinfo("Expense Summary", summary)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseApp(root)
    root.mainloop()