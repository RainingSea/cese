import tkinter as tk
from tkinter import messagebox, Listbox, Entry, Button
from inventory_manager import InventoryManager

class Main:
    def __init__(self) -> None:
        self.inventory_manager = InventoryManager('inventory.json')
        self.root = tk.Tk()
        self.root.title("Office Stock Manager")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self) -> None:
        self.item_name_entry = Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Item Name").grid(row=0, column=0)

        self.category_entry = Entry(self.root)
        self.category_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Category").grid(row=1, column=0)

        self.quantity_entry = Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)
        tk.Label(self.root, text="Quantity").grid(row=2, column=0)

        self.add_button = Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=3, column=0)

        self.update_button = Button(self.root, text="Update Item", command=self.update_item)
        self.update_button.grid(row=3, column=1)

        self.search_entry = Entry(self.root)
        self.search_entry.grid(row=4, column=1)
        tk.Label(self.root, text="Search Item").grid(row=4, column=0)

        self.search_button = Button(self.root, text="Search", command=self.search_item)
        self.search_button.grid(row=5, column=0)

        self.listbox = Listbox(self.root)
        self.listbox.grid(row=6, column=0, columnspan=2)

        self.load_inventory()

    def add_item(self) -> None:
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.add_item(name, category, quantity)
        self.load_inventory()

    def update_item(self) -> None:
        name = self.item_name_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.update_item(name, quantity)
        self.load_inventory()

    def search_item(self) -> None:
        name = self.search_entry.get()
        item = self.inventory_manager.search_item(name)
        if item:
            messagebox.showinfo("Item Found", f"Name: {item['name']}, Category: {item['category']}, Quantity: {item['quantity']}")
        else:
            messagebox.showwarning("Item Not Found", "No item found with that name.")

    def load_inventory(self) -> None:
        self.listbox.delete(0, tk.END)
        for item in self.inventory_manager.items:
            self.listbox.insert(tk.END, f"{item['name']} | {item['category']} | {item['quantity']}")

if __name__ == "__main__":
    Main()