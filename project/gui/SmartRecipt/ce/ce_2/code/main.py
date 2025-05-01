import tkinter as tk
from tkinter import messagebox
from search_engine import SearchEngine

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Receipt Manager")
        
        self.search_engine = SearchEngine()
        self.create_widgets()
        
    def create_widgets(self):
        # Date input
        self.date_label = tk.Label(self.master, text="Date (YYYY-MM-DD):")
        self.date_label.pack()
        self.date_entry = tk.Entry(self.master)
        self.date_entry.pack()

        # Merchant input
        self.merchant_label = tk.Label(self.master, text="Merchant Name:")
        self.merchant_label.pack()
        self.merchant_entry = tk.Entry(self.master)
        self.merchant_entry.pack()

        # Total amount input
        self.amount_label = tk.Label(self.master, text="Total Amount:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.master)
        self.amount_entry.pack()

        # Submit button
        self.submit_button = tk.Button(self.master, text="Submit Receipt", command=self.submit_receipt)
        self.submit_button.pack()

        # Search bar
        self.search_label = tk.Label(self.master, text="Search Receipts:")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack()

        # Search button
        self.search_button = tk.Button(self.master, text="Search", command=self.search_receipts)
        self.search_button.pack()

    def submit_receipt(self):
        date = self.date_entry.get()
        merchant = self.merchant_entry.get()
        total_amount = self.amount_entry.get()

        if not date or not merchant or not total_amount:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            total_amount = float(total_amount)
        except ValueError:
            messagebox.showerror("Input Error", "Total amount must be a number.")
            return

        self.search_engine.add_receipt(date, merchant, total_amount)
        self.clear_entries()
        messagebox.showinfo("Success", "Receipt added successfully.")

    def search_receipts(self):
        query = self.search_entry.get()
        results = self.search_engine.search_receipts(query)
        
        if results:
            messagebox.showinfo("Search Results", "\n".join(results))
        else:
            messagebox.showinfo("Search Results", "No receipts found.")

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.merchant_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    @staticmethod
    def main():
        root = tk.Tk()
        app = Main(root)
        root.mainloop()

if __name__ == "__main__":
    Main.main()