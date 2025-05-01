import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from datetime import datetime
import os

class Receipt:
    def __init__(self, date: str, merchant: str, total_amount: float):
        self.date = date
        self.merchant = merchant
        self.total_amount = total_amount

    def to_string(self) -> str:
        return f"{self.date}|{self.merchant}|{self.total_amount:.2f}"

class ReceiptManager:
    def __init__(self):
        self.receipts = self.load_receipts()

    def add_receipt(self, receipt: Receipt) -> None:
        self.receipts.append(receipt)
        self.save_receipts()

    def search_receipts(self, criteria: dict) -> list:
        results = []
        for receipt in self.receipts:
            if all(getattr(receipt, key) == value for key, value in criteria.items() if value is not None):
                results.append(receipt)
        return results

    def load_receipts(self) -> list:
        receipts = []
        if os.path.exists('receipts.txt'):
            with open('receipts.txt', 'r') as file:
                for line in file:
                    date, merchant, total_amount = line.strip().split('|')
                    receipts.append(Receipt(date, merchant, float(total_amount)))
        return receipts

    def save_receipts(self) -> None:
        with open('receipts.txt', 'w') as file:
            for receipt in self.receipts:
                file.write(receipt.to_string() + '\n')

    def validate_date(self, date: str) -> bool:
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_amount(self, amount: str) -> bool:
        try:
            float(amount)
            return True
        except ValueError:
            return False

class Main:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Receipt Manager")
        self.receipt_manager = ReceiptManager()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Merchant Name:").grid(row=1, column=0)
        self.merchant_entry = tk.Entry(self.root)
        self.merchant_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Total Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Receipt", command=self.add_receipt)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.search_button = tk.Button(self.root, text="Search Receipts", command=self.search_receipts)
        self.search_button.grid(row=4, column=0, columnspan=2)

        self.receipt_listbox = Listbox(self.root)
        self.receipt_listbox.grid(row=5, column=0, columnspan=2)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=5, column=2)
        self.receipt_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.receipt_listbox.yview)

        self.update_receipt_listbox()

    def add_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        amount = self.amount_entry.get()

        if not self.receipt_manager.validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return
        if not self.receipt_manager.validate_amount(amount):
            messagebox.showerror("Error", "Invalid amount format.")
            return

        receipt = Receipt(date, merchant, float(amount))
        self.receipt_manager.add_receipt(receipt)
        self.update_receipt_listbox()
        messagebox.showinfo("Success", "Receipt added successfully!")

    def search_receipts(self):
        criteria = {
            'date': self.date_entry.get(),
            'merchant': self.merchant_entry.get(),
            'total_amount': float(self.amount_entry.get()) if self.amount_entry.get() else None
        }
        results = self.receipt_manager.search_receipts(criteria)
        self.receipt_listbox.delete(0, tk.END)
        for receipt in results:
            self.receipt_listbox.insert(tk.END, receipt.to_string())

    def update_receipt_listbox(self):
        self.receipt_listbox.delete(0, tk.END)
        for receipt in self.receipt_manager.receipts:
            self.receipt_listbox.insert(tk.END, receipt.to_string())

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application closed."

if __name__ == "__main__":
    main()