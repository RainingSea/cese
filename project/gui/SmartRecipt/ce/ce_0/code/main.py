import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from receipt_manager import ReceiptManager

class Main:
    def __init__(self):
        self.receipt_manager = ReceiptManager('receipts.txt')
        self.root = tk.Tk()
        self.root.title("Smart Receipt Application")
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
        self.add_button.grid(row=3, columnspan=2)

        tk.Label(self.root, text="Search:").grid(row=4, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=4, column=1)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_receipts)
        self.search_button.grid(row=5, columnspan=2)

        self.result_listbox = Listbox(self.root)
        self.result_listbox.grid(row=6, columnspan=2)

        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=6, column=2, sticky='ns')
        self.result_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result_listbox.yview)

    def add_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total = self.amount_entry.get()
        try:
            total = float(total)
            self.receipt_manager.add_receipt(date, merchant, total)
            messagebox.showinfo("Success", "Receipt added successfully!")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Total amount must be a number.")

    def search_receipts(self):
        query = self.search_entry.get()
        results = self.receipt_manager.search_receipts(query)
        self.result_listbox.delete(0, tk.END)
        for receipt in results:
            self.result_listbox.insert(tk.END, receipt)

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.merchant_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def main(self) -> str:
        self.root.mainloop()
        return "Application closed."

if __name__ == "__main__":
    app = Main()
    app.main()