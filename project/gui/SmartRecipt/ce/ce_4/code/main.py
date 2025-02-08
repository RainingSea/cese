import tkinter as tk
from tkinter import messagebox
from receipt_manager import ReceiptManager

class Main:
    def __init__(self):
        self.receipt_manager = ReceiptManager("receipts.txt")
        self.root = tk.Tk()
        self.root.title("Smart Receipt Application")
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)

        self.merchant_entry = tk.Entry(self.root)
        self.merchant_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Merchant Name:").grid(row=1, column=0)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=2, column=1)
        tk.Label(self.root, text="Total Amount:").grid(row=2, column=0)

        # Submit button
        submit_button = tk.Button(self.root, text="Add Receipt", command=self.add_receipt)
        submit_button.grid(row=3, columnspan=2)

        # Search fields
        self.search_date_entry = tk.Entry(self.root)
        self.search_date_entry.grid(row=4, column=1)
        tk.Label(self.root, text="Search Date:").grid(row=4, column=0)

        self.search_merchant_entry = tk.Entry(self.root)
        self.search_merchant_entry.grid(row=5, column=1)
        tk.Label(self.root, text="Search Merchant:").grid(row=5, column=0)

        self.search_amount_entry = tk.Entry(self.root)
        self.search_amount_entry.grid(row=6, column=1)
        tk.Label(self.root, text="Search Amount:").grid(row=6, column=0)

        # Search button
        search_button = tk.Button(self.root, text="Search Receipts", command=self.search_receipts)
        search_button.grid(row=7, columnspan=2)

        # Display area
        self.result_area = tk.Text(self.root, height=10, width=50)
        self.result_area.grid(row=8, columnspan=2)

    def add_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total_amount = self.amount_entry.get()

        if not date or not merchant or not total_amount:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        try:
            total_amount = float(total_amount)
            self.receipt_manager.add_receipt(date, merchant, total_amount)
            messagebox.showinfo("Success", "Receipt added successfully.")
        except ValueError:
            messagebox.showerror("Input Error", "Total amount must be a number.")

    def search_receipts(self):
        date = self.search_date_entry.get()
        merchant = self.search_merchant_entry.get()
        total_amount = self.search_amount_entry.get()

        total_amount = float(total_amount) if total_amount else None

        results = self.receipt_manager.search_receipts(date, merchant, total_amount)
        self.result_area.delete(1.0, tk.END)  # Clear previous results

        if not results:
            self.result_area.insert(tk.END, "No receipts found.\n")
        else:
            for receipt in results:
                self.result_area.insert(tk.END, f"{receipt[0]}, {receipt[1]}, {receipt[2]}\n")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()