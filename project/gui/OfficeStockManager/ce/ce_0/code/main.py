import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar, END
from inventory_manager import InventoryManager

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Stock Manager")
        self.inventory_manager = InventoryManager('inventory.txt')

        self.create_widgets()
        self.populate_inventory()

    def create_widgets(self):
        """Creates the main GUI components."""
        self.item_name_label = tk.Label(self.root, text="Item Name:")
        self.item_name_label.grid(row=0, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.update_button = tk.Button(self.root, text="Update Item", command=self.update_item)
        self.update_button.grid(row=4, column=0, columnspan=2)

        self.search_label = tk.Label(self.root, text="Search:")
        self.search_label.grid(row=5, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=5, column=1)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_item)
        self.search_button.grid(row=5, column=2)

        self.inventory_listbox = Listbox(self.root)
        self.inventory_listbox.grid(row=6, column=0, columnspan=3)
        self.scrollbar = Scrollbar(self.root)
        self.scrollbar.grid(row=6, column=3)
        self.inventory_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.inventory_listbox.yview)

    def populate_inventory(self):
        """Populates the inventory listbox with items."""
        self.inventory_listbox.delete(0, END)
        for item in self.inventory_manager.items:
            self.inventory_listbox.insert(END, f"{item[0]} ({item[1]}): {item[2]}")

    def add_item(self):
        """Handles the addition of a new item to the inventory."""
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        quantity = self.quantity_entry.get()
        if name and category and quantity.isdigit():
            self.inventory_manager.add_item(name, category, int(quantity))
            self.populate_inventory()
            self.clear_entries()
        else:
            messagebox.showerror("Input Error", "Please enter valid item details.")

    def update_item(self):
        """Handles the update of stock quantity for an existing item."""
        selected_item = self.inventory_listbox.curselection()
        if selected_item:
            item_details = self.inventory_listbox.get(selected_item).split(':')
            name = item_details[0].split('(')[0].strip()
            quantity = self.quantity_entry.get()
            if quantity.isdigit():
                self.inventory_manager.update_item(name, int(quantity))
                self.populate_inventory()
                self.clear_entries()
            else:
                messagebox.showerror("Input Error", "Please enter a valid quantity.")
        else:
            messagebox.showerror("Selection Error", "Please select an item to update.")

    def search_item(self):
        """Handles the search functionality to retrieve specific item information."""
        query = self.search_entry.get()
        results = self.inventory_manager.search_item(query)
        self.inventory_listbox.delete(0, END)
        for item in results:
            self.inventory_listbox.insert(END, f"{item[0]} ({item[1]}): {item[2]}")

    def clear_entries(self):
        """Clears input fields."""
        self.item_name_entry.delete(0, END)
        self.category_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.search_entry.delete(0, END)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()