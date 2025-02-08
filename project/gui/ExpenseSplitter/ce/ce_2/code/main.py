import tkinter as tk
from tkinter import messagebox
from ExpenseSplitter import ExpenseSplitter

class ExpenseSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter")
        self.splitter = ExpenseSplitter()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Total Amount:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Participants (comma separated):").grid(row=1, column=0)
        self.participants_entry = tk.Entry(self.root)
        self.participants_entry.grid(row=1, column=1)

        self.submit_button = tk.Button(self.root, text="Submit Expense", command=self.submit_expense)
        self.submit_button.grid(row=2, columnspan=2)

        self.view_button = tk.Button(self.root, text="View Shares", command=self.view_shares)
        self.view_button.grid(row=3, columnspan=2)

        self.result_display = tk.Text(self.root, height=10, width=50)
        self.result_display.grid(row=4, columnspan=2)

    def submit_expense(self):
        try:
            total_amount = float(self.amount_entry.get())
            participants = self.participants_entry.get().split(',')
            participants = [name.strip() for name in participants]
            self.splitter.add_expense(total_amount, participants)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def view_shares(self):
        shares = self.splitter.calculate_shares()
        self.result_display.delete(1.0, tk.END)
        for participant, share in shares.items():
            self.result_display.insert(tk.END, f"{participant}: {share:.2f}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSplitterApp(root)
    root.mainloop()