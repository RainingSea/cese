import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class Main:
    def __init__(self):
        self.shopping_list_manager = ShoppingListManager()
        self.root = tk.Tk()
        self.root.title("Shopping Planner")
        self.setup_ui()

    def setup_ui(self):
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

        self.item_entry = tk.Entry(self.root, width=40)
        self.item_entry.pack(pady=5)

        self.category_entry = tk.Entry(self.root, width=40)
        self.category_entry.pack(pady=5)

        add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        add_button.pack(pady=5)

        import_button = tk.Button(self.root, text="Import Items", command=self.import_items)
        import_button.pack(pady=5)

        self.load_categories()

    def load_categories(self):
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                categories = file.readlines()
                self.categories = [category.strip() for category in categories]
        else:
            self.categories = []

    def add_item(self):
        item = self.item_entry.get()
        category = self.category_entry.get()
        if item and category:
            self.shopping_list_manager.add_item(item, category)
            self.update_listbox()
            self.item_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter both item and category.")

    def import_items(self):
        file_path = simpledialog.askstring("Import Items", "Enter the file path:")
        if file_path:
            self.shopping_list_manager.import_items(file_path)
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.shopping_list_manager.get_items():
            self.listbox.insert(tk.END, item)

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()