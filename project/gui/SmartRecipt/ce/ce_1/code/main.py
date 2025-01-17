import tkinter as tk
from tkinter import messagebox
import os

class ReceiptManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_receipts()

    def add_receipt(self, date: str, merchant: str, total_amount: float) -> None:
        with open(self.file_path, 'a') as file:
            file.write(f"{date},{merchant},{total_amount}\n")
        self.load_receipts()  # Reload receipts after adding

    def search_receipts(self, date: str = "", merchant: str = "", total_amount: float = None) -> list:
        results = []
        for receipt in self.receipts:
            receipt_date, receipt_merchant, receipt_amount = receipt.split(',')
            if (date in receipt_date) and (merchant in receipt_merchant) and (str(total_amount) in receipt_amount):
                results.append(receipt)
        return results

    def load_receipts(self) -> list:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.receipts = file.read().strip().splitlines()
        else:
            self.receipts = []

class Main:
    def __init__(self, master):
        self.master = master
        master.title("Smart Receipt Application")

        self.receipt_manager = ReceiptManager("receipts.txt")

        self.date_label = tk.Label(master, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(master)
        self.date_entry.pack()

        self.merchant_label = tk.Label(master, text="Merchant:")
        self.merchant_label.pack()
        self.merchant_entry = tk.Entry(master)
        self.merchant_entry.pack()

        self.amount_label = tk.Label(master, text="Total Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack()

        self.add_button = tk.Button(master, text="Add Receipt", command=self.add_receipt)
        self.add_button.pack()

        self.search_label = tk.Label(master, text="Search Receipts:")
        self.search_label.pack()
        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_receipts)
        self.search_button.pack()

        self.result_listbox = tk.Listbox(master)
        self.result_listbox.pack()

        self.load_receipts()

    def add_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total_amount = self.amount_entry.get()
        try:
            total_amount = float(total_amount)
            self.receipt_manager.add_receipt(date, merchant, total_amount)
            messagebox.showinfo("Success", "Receipt added successfully!")
            self.load_receipts()
        except ValueError:
            messagebox.showerror("Error", "Total amount must be a number.")

    def search_receipts(self):
        search_query = self.search_entry.get()
        results = self.receipt_manager.search_receipts(merchant=search_query)
        self.result_listbox.delete(0, tk.END)
        for result in results:
            self.result_listbox.insert(tk.END, result)

    def load_receipts(self):
        self.result_listbox.delete(0, tk.END)
        for receipt in self.receipt_manager.receipts:
            self.result_listbox.insert(tk.END, receipt)

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()