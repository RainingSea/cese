import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class InventoryManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.items = []
        self.load_items()

    def load_items(self) -> None:
        try:
            with open(self.file_path, 'r') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            self.items = []

    def save_items(self) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(self.items, file, indent=4)

    def add_item(self, name: str, category: str, quantity: int) -> None:
        self.items.append({"name": name, "category": category, "quantity": quantity})
        self.save_items()

    def update_item(self, name: str, quantity: int) -> None:
        for item in self.items:
            if item["name"] == name:
                item["quantity"] = quantity
                self.save_items()
                return
        messagebox.showerror("Error", "Item not found.")

    def search_item(self, query: str) -> list:
        return [item for item in self.items if query.lower() in item["name"].lower()]

class GUI:
    def __init__(self, inventory_manager: InventoryManager):
        self.inventory_manager = inventory_manager
        self.root = tk.Tk()
        self.create_main_window()

    def create_main_window(self) -> None:
        self.root.title("Office Stock Manager")

        self.name_label = tk.Label(self.root, text="Item Name")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.category_label = tk.Label(self.root, text="Category")
        self.category_label.pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()

        self.quantity_label = tk.Label(self.root, text="Quantity")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item_ui)
        self.add_button.pack()

        self.update_button = tk.Button(self.root, text="Update Item", command=self.update_item_ui)
        self.update_button.pack()

        self.search_label = tk.Label(self.root, text="Search")
        self.search_label.pack()
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.search_item_ui)
        self.search_button.pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.display_items()
        self.root.mainloop()

    def add_item_ui(self) -> None:
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.add_item(name, category, quantity)
        self.display_items()

    def update_item_ui(self) -> None:
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.update_item(name, quantity)
        self.display_items()

    def search_item_ui(self) -> None:
        query = self.search_entry.get()
        results = self.inventory_manager.search_item(query)
        self.listbox.delete(0, tk.END)
        for item in results:
            self.listbox.insert(tk.END, f"{item['name']} - {item['category']} - {item['quantity']}")

    def display_items(self) -> None:
        self.listbox.delete(0, tk.END)
        for item in self.inventory_manager.items:
            self.listbox.insert(tk.END, f"{item['name']} - {item['category']} - {item['quantity']}")

if __name__ == "__main__":
    inventory_manager = InventoryManager("inventory.json")
    gui = GUI(inventory_manager)