import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager
from data_handler import Item

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Office Supplies Inventory")
        self.inventory_manager = InventoryManager()

        self.item_name_label = tk.Label(master, text="Item Name:")
        self.item_name_label.pack()
        self.item_name_entry = tk.Entry(master)
        self.item_name_entry.pack()

        self.category_label = tk.Label(master, text="Category:")
        self.category_label.pack()
        self.category_entry = tk.Entry(master)
        self.category_entry.pack()

        self.quantity_label = tk.Label(master, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(master)
        self.quantity_entry.pack()

        self.add_button = tk.Button(master, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.update_button = tk.Button(master, text="Update Quantity", command=self.update_quantity)
        self.update_button.pack()

        self.search_button = tk.Button(master, text="Search Item", command=self.search_item)
        self.search_button.pack()

        self.search_all_button = tk.Button(master, text="Search Items", command=self.search_items)
        self.search_all_button.pack()

        self.display_area = tk.Text(master)
        self.display_area.pack()

    def add_item(self):
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        try:
            item = Item(name, category, quantity)
            self.inventory_manager.add_item(item)
            messagebox.showinfo("Success", "Item added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def update_quantity(self):
        name = self.item_name_entry.get()
        quantity = int(self.quantity_entry.get())
        try:
            self.inventory_manager.update_quantity(name, quantity)
            messagebox.showinfo("Success", "Quantity updated successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_item(self):
        name = self.item_name_entry.get()
        try:
            item = self.inventory_manager.search_item(name)
            self.display_area.delete(1.0, tk.END)
            self.display_area.insert(tk.END, f"Name: {item._name}\nCategory: {item._category}\nQuantity: {item._quantity}")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def search_items(self):
        query = self.item_name_entry.get()
        items = self.inventory_manager.search_items(query)
        self.display_area.delete(1.0, tk.END)
        if items:
            for item in items:
                self.display_area.insert(tk.END, f"Name: {item._name}, Category: {item._category}, Quantity: {item._quantity}\n")
        else:
            self.display_area.insert(tk.END, "No items found.")

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()