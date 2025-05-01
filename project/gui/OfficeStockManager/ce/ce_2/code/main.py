import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self, root):
        self.inventory_manager = InventoryManager()
        self.root = root
        self.root.title("Office Stock Manager")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Item Name").grid(row=0, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category").grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Quantity").grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Description").grid(row=3, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=4, column=0)
        tk.Button(self.root, text="Update Quantity", command=self.update_quantity).grid(row=4, column=1)
        tk.Button(self.root, text="Search Item", command=self.search_item).grid(row=4, column=2)

        self.inventory_display = tk.Listbox(self.root)
        self.inventory_display.grid(row=5, column=0, columnspan=3)

    def add_item(self):
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        description = self.description_entry.get()
        self.inventory_manager.add_item(name, category, quantity, description)
        self.update_inventory_display()

    def update_quantity(self):
        name = self.item_name_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.update_quantity(name, quantity)
        self.update_inventory_display()

    def search_item(self):
        name = self.item_name_entry.get()
        item = self.inventory_manager.search_item(name)
        if item:
            messagebox.showinfo("Item Found", f"Name: {item.name}\nCategory: {item.category}\nQuantity: {item.quantity}\nDescription: {item.description}")
        else:
            messagebox.showwarning("Item Not Found", "The item does not exist in the inventory.")

    def update_inventory_display(self):
        self.inventory_display.delete(0, tk.END)
        for item in self.inventory_manager.items:
            self.inventory_display.insert(tk.END, f"{item.name} - {item.category} - {item.quantity} - {item.description}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()