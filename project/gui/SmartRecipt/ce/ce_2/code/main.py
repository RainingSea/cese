import tkinter as tk
from tkinter import messagebox, Listbox
from ReceiptManager import ReceiptManager

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Receipt Management Application")
        self.receipt_manager = ReceiptManager()

        self.date_label = tk.Label(master, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(master)
        self.date_entry.pack()

        self.merchant_label = tk.Label(master, text="Merchant Name:")
        self.merchant_label.pack()
        self.merchant_entry = tk.Entry(master)
        self.merchant_entry.pack()

        self.amount_label = tk.Label(master, text="Total Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(master)
        self.amount_entry.pack()

        self.save_button = tk.Button(master, text="Save Receipt", command=self.save_receipt)
        self.save_button.pack()

        self.search_label = tk.Label(master, text="Search Receipts:")
        self.search_label.pack()
        self.search_entry = tk.Entry(master)
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_receipts)
        self.search_button.pack()

        self.results_listbox = Listbox(master)
        self.results_listbox.pack()

    def save_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        try:
            total_amount = float(self.amount_entry.get())
            self.receipt_manager.save_receipt(date, merchant, total_amount)
            messagebox.showinfo("Success", "Receipt saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def search_receipts(self):
        query = self.search_entry.get()
        results = self.receipt_manager.search_receipts(query)
        self.results_listbox.delete(0, tk.END)
        for result in results:
            self.results_listbox.insert(tk.END, result)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()