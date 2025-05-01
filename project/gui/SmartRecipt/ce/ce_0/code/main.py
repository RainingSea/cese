import tkinter as tk
from tkinter import messagebox
import os

class Receipt:
    def __init__(self, date: str, merchant: str, total_amount: float):
        self.date = date
        self.merchant = merchant
        self.total_amount = total_amount

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Receipt Manager")
        self.receipts = self.load_receipts()

        self.create_widgets()

    def create_widgets(self):
        # Input form
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Merchant Name:").grid(row=1, column=0)
        self.merchant_entry = tk.Entry(self.root)
        self.merchant_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Total Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Receipt", command=self.save_receipt)
        self.save_button.grid(row=3, columnspan=2)

        # Search bar
        tk.Label(self.root, text="Search Receipts:").grid(row=4, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=4, column=1)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_receipts)
        self.search_button.grid(row=5, columnspan=2)

        # Display area
        self.results_text = tk.Text(self.root, height=10, width=50)
        self.results_text.grid(row=6, columnspan=2)

    def main(self):
        self.root.mainloop()

    def add_receipt(self, date: str, merchant: str, total_amount: float):
        receipt = Receipt(date, merchant, total_amount)
        self.receipts.append(receipt)
        self.save_receipts_to_file()

    def save_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total_amount = float(self.amount_entry.get())
        
        self.add_receipt(date, merchant, total_amount)
        messagebox.showinfo("Success", "Receipt saved successfully!")

    def search_receipts(self, query: str):
        results = [f"{r.date}, {r.merchant}, {r.total_amount}" for r in self.receipts if query in r.date or query in r.merchant or query in str(r.total_amount)]
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n".join(results) if results else "No receipts found.")

    def load_receipts(self):
        if not os.path.exists('receipts.txt'):
            return []
        with open('receipts.txt', 'r') as file:
            return [Receipt(*line.strip().split(',')) for line in file.readlines()]

    def save_receipts_to_file(self):
        with open('receipts.txt', 'w') as file:
            for receipt in self.receipts:
                file.write(f"{receipt.date},{receipt.merchant},{receipt.total_amount}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.main()