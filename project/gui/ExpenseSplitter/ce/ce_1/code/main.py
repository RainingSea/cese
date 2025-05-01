import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter")
        self.expense_splitter = ExpenseSplitter()

        self.total_entry = tk.Entry(root)
        self.total_entry.pack(pady=10)
        self.total_entry.insert(0, "Enter total expense")

        self.names_entry = tk.Entry(root)
        self.names_entry.pack(pady=10)
        self.names_entry.insert(0, "Enter names separated by commas")

        self.submit_button = tk.Button(root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.pack(pady=10)

        self.results_text = tk.Text(root, height=10, width=50)
        self.results_text.pack(pady=10)

        self.previous_expenses_button = tk.Button(root, text="Show Previous Expenses", command=self.display_results)
        self.previous_expenses_button.pack(pady=10)

    def submit_expense(self) -> None:
        try:
            total = float(self.total_entry.get())
            names = self.names_entry.get().split(',')
            self.expense_splitter.add_expense(total, names)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.total_entry.delete(0, tk.END)
            self.names_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid total expense.")

    def display_results(self) -> None:
        shares = self.expense_splitter.calculate_shares()
        self.results_text.delete(1.0, tk.END)
        for name, share in shares.items():
            self.results_text.insert(tk.END, f"{name}: {share:.2f}\n")

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()