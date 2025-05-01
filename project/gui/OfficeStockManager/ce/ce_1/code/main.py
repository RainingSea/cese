import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from typing import List

class Item:
    def __init__(self, name: str, category: str, quantity: int):
        self.name = name
        self.category = category
        self.quantity = quantity

class InventoryManager:
    def __init__(self):
        self.items = []
        self.load_inventory()

    def add_item(self, name: str, category: str, quantity: int) -> None:
        new_item = Item(name, category, quantity)
        self.items.append(new_item)
        self.save_inventory()

    def update_item(self, name: str, quantity: int) -> None:
        for item in self.items:
            if item.name == name:
                item.quantity = quantity
                self.save_inventory()
                return
        messagebox.showerror("Error", "Item not found.")

    def search_item(self, query: str) -> List[Item]:
        return [item for item in self.items if query.lower() in item.name.lower()]

    def load_inventory(self) -> None:
        try:
            with open('inventory.txt', 'r') as file:
                for line in file:
                    name, category, quantity = line.strip().split(',')
                    self.items.append(Item(name, category, int(quantity)))
        except FileNotFoundError:
            open('inventory.txt', 'w').close()  # Create file if it doesn't exist

    def save_inventory(self) -> None:
        with open('inventory.txt', 'w') as file:
            for item in self.items:
                file.write(f"{item.name},{item.category},{item.quantity}\n")

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Stock Manager")
        self.inventory_manager = InventoryManager()
        self.create_widgets()

    def create_widgets(self):
        self.name_entry = tk.Entry(self.root)
        self.category_entry = tk.Entry(self.root)
        self.quantity_entry = tk.Entry(self.root)
        self.search_entry = tk.Entry(self.root)
        self.listbox = Listbox(self.root)
        self.scrollbar = Scrollbar(self.root)

        self.name_entry.grid(row=0, column=1)
        self.category_entry.grid(row=1, column=1)
        self.quantity_entry.grid(row=2, column=1)
        self.search_entry.grid(row=3, column=1)
        self.listbox.grid(row=4, column=0, columnspan=2)
        self.scrollbar.grid(row=4, column=2)

        tk.Label(self.root, text="Item Name").grid(row=0, column=0)
        tk.Label(self.root, text="Category").grid(row=1, column=0)
        tk.Label(self.root, text="Quantity").grid(row=2, column=0)
        tk.Label(self.root, text="Search").grid(row=3, column=0)

        tk.Button(self.root, text="Add Item", command=self.add_item).grid(row=5, column=0)
        tk.Button(self.root, text="Update Item", command=self.update_item).grid(row=5, column=1)
        tk.Button(self.root, text="Search", command=self.search_item).grid(row=6, column=0, columnspan=2)

        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

    def add_item(self):
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.add_item(name, category, quantity)
        messagebox.showinfo("Success", "Item added successfully.")
        self.clear_entries()

    def update_item(self):
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.update_item(name, quantity)
        messagebox.showinfo("Success", "Item updated successfully.")
        self.clear_entries()

    def search_item(self):
        query = self.search_entry.get()
        results = self.inventory_manager.search_item(query)
        self.listbox.delete(0, tk.END)
        for item in results:
            self.listbox.insert(tk.END, f"{item.name} | {item.category} | {item.quantity}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()