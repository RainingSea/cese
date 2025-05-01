import tkinter as tk
from tkinter import messagebox
import os

class ReceiptManager:
    def __init__(self):
        self.receipts = []
        self.load_receipts()

    def add_receipt(self, date: str, merchant: str, total: float) -> None:
        receipt = f"{date},{merchant},{total}"
        self.receipts.append(receipt)
        self.save_receipts()

    def search_receipts(self, query: str) -> list:
        return [receipt for receipt in self.receipts if query in receipt]

    def load_receipts(self) -> None:
        if os.path.exists('receipts.txt'):
            with open('receipts.txt', 'r') as file:
                self.receipts = [line.strip() for line in file.readlines()]

    def save_receipts(self) -> None:
        with open('receipts.txt', 'w') as file:
            for receipt in self.receipts:
                file.write(receipt + '\n')

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Receipt Manager")
        self.receipt_manager = ReceiptManager()

        self.date_label = tk.Label(master, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(master)
        self.date_entry.pack()

        self.merchant_label = tk.Label(master, text="Merchant:")
        self.merchant_label.pack()
        self.merchant_entry = tk.Entry(master)
        self.merchant_entry.pack()

        self.total_label = tk.Label(master, text="Total Amount:")
        self.total_label.pack()
        self.total_entry = tk.Entry(master)
        self.total_entry.pack()

        self.save_button = tk.Button(master, text="Save Receipt", command=self.save_receipt)
        self.save_button.pack()

        self.search_label = tk.Label(master, text="Search Receipts:")
        self.search_label.pack()
        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_receipts)
        self.search_button.pack()

        self.results_label = tk.Label(master, text="Results:")
        self.results_label.pack()
        self.results_display = tk.Text(master, height=10, width=50)
        self.results_display.pack()

    def save_receipt(self) -> None:
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total = self.total_entry.get()

        try:
            total = float(total)
            self.receipt_manager.add_receipt(date, merchant, total)
            messagebox.showinfo("Success", "Receipt saved successfully!")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Invalid total amount. Please enter a number.")

    def search_receipts(self) -> None:
        query = self.search_entry.get()
        results = self.receipt_manager.search_receipts(query)
        self.results_display.delete(1.0, tk.END)
        if results:
            for receipt in results:
                self.results_display.insert(tk.END, receipt + '\n')
        else:
            self.results_display.insert(tk.END, "No matching receipts found.")

    def clear_entries(self) -> None:
        self.date_entry.delete(0, tk.END)
        self.merchant_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
    return "Application Closed"

if __name__ == "__main__":
    main()