import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self):
        self.inventory_manager = InventoryManager('inventory.txt')
        self.root = tk.Tk()
        self.root.title("Office Stock Manager")
        self.create_widgets()

    def create_widgets(self):
        self.item_name_label = tk.Label(self.root, text="Item Name:")
        self.item_name_label.grid(row=0, column=0)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.grid(row=0, column=1)

        self.item_type_label = tk.Label(self.root, text="Item Type:")
        self.item_type_label.grid(row=1, column=0)
        self.item_type_entry = tk.Entry(self.root)
        self.item_type_entry.grid(row=1, column=1)

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.grid(row=3, column=0)

        self.update_button = tk.Button(self.root, text="Update Quantity", command=self.update_item)
        self.update_button.grid(row=3, column=1)

        self.search_label = tk.Label(self.root, text="Search Item:")
        self.search_label.grid(row=4, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=4, column=1)

        self.search_button = tk.Button(self.root, text="Search", command=self.search_item)
        self.search_button.grid(row=5, column=0)

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.grid(row=6, column=0, columnspan=2)

        self.load_inventory()

    def add_item(self):
        item_name = self.item_name_entry.get()
        item_type = self.item_type_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.add_item(item_name, item_type, quantity)
        self.load_inventory()
        messagebox.showinfo("Success", "Item added successfully!")

    def update_item(self):
        item_name = self.item_name_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.update_quantity(item_name, quantity)
        self.load_inventory()
        messagebox.showinfo("Success", "Item updated successfully!")

    def search_item(self):
        item_name = self.search_entry.get()
        item = self.inventory_manager.search_item(item_name)
        if item:
            messagebox.showinfo("Item Found", f"Name: {item['item_name']}, Type: {item['item_type']}, Quantity: {item['quantity']}")
        else:
            messagebox.showinfo("Not Found", "Item not found.")

    def load_inventory(self):
        self.listbox.delete(0, tk.END)
        for item in self.inventory_manager.inventory:
            self.listbox.insert(tk.END, f"{item['item_name']} - {item['item_type']} - {item['quantity']}")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()