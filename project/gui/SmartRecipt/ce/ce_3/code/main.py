import tkinter as tk
from tkinter import messagebox, Listbox
import os

class ReceiptManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_receipts()

    def add_receipt(self, date: str, merchant: str, total_amount: float):
        with open(self.file_path, 'a') as file:
            file.write(f"{date},{merchant},{total_amount}\n")
        self.load_receipts()

    def search_receipts(self, date: str = "", merchant: str = "", total_amount: float = None) -> list:
        results = []
        for receipt in self.receipts:
            receipt_date, receipt_merchant, receipt_total = receipt.strip().split(',')
            if (date == "" or receipt_date == date) and \
               (merchant == "" or receipt_merchant == merchant) and \
               (total_amount is None or float(receipt_total) == total_amount):
                results.append(receipt)
        return results

    def load_receipts(self) -> list:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.receipts = file.readlines()
        else:
            self.receipts = []

class Main:
    def __init__(self):
        self.receipt_manager = ReceiptManager('receipts.txt')
        self.setup_ui()

    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Smart Receipt Application")

        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Merchant Name:").grid(row=1, column=0)
        self.merchant_entry = tk.Entry(self.root)
        self.merchant_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Total Amount:").grid(row=2, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)

        self.save_button = tk.Button(self.root, text="Save Receipt", command=self.save_receipt)
        self.save_button.grid(row=3, column=0, columnspan=2)

        self.search_button = tk.Button(self.root, text="Search Receipts", command=self.search_receipts)
        self.search_button.grid(row=4, column=0, columnspan=2)

        self.results_listbox = Listbox(self.root)
        self.results_listbox.grid(row=5, column=0, columnspan=2)

        self.root.mainloop()

    def save_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        try:
            total_amount = float(self.amount_entry.get())
            self.receipt_manager.add_receipt(date, merchant, total_amount)
            messagebox.showinfo("Success", "Receipt saved successfully.")
        except ValueError:
            messagebox.showerror("Error", "Total amount must be a number.")

    def search_receipts(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        try:
            total_amount = float(self.amount_entry.get())
        except ValueError:
            total_amount = None

        results = self.receipt_manager.search_receipts(date, merchant, total_amount)
        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result.strip())

if __name__ == "__main__":
    Main()