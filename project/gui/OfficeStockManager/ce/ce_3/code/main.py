import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self) -> None:
        self.inventory_manager = InventoryManager()
        self.inventory_manager.load_inventory('inventory.json')
        self.root = tk.Tk()
        self.root.title("Office Stock Manager")
        self.create_widgets()

    def create_widgets(self) -> None:
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        add_button.pack()

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack()
        self.update_listbox()

        search_entry = tk.Entry(self.root)
        search_entry.pack()
        search_button = tk.Button(self.root, text="Search", command=lambda: self.search_item(search_entry.get()))
        search_button.pack()

        update_button = tk.Button(self.root, text="Update Quantity", command=self.update_quantity)
        update_button.pack()

    def add_item(self) -> None:
        name = self.name_entry.get()
        category = self.category_entry.get()
        quantity = int(self.quantity_entry.get())
        self.inventory_manager.add_item(name, category, quantity)
        self.update_listbox()
        self.inventory_manager.save_inventory('inventory.json')

    def update_quantity(self) -> None:
        selected_item = self.listbox.curselection()
        if selected_item:
            item_name = self.listbox.get(selected_item)
            new_quantity = int(self.quantity_entry.get())
            self.inventory_manager.update_item(item_name, new_quantity)
            self.update_listbox()
            self.inventory_manager.save_inventory('inventory.json')
        else:
            messagebox.showwarning("Selection Error", "No item selected.")

    def search_item(self, query: str) -> None:
        results = self.inventory_manager.search_item(query)
        self.listbox.delete(0, tk.END)
        for item in results:
            self.listbox.insert(tk.END, item.name)

    def update_listbox(self) -> None:
        self.listbox.delete(0, tk.END)
        for item in self.inventory_manager.items:
            self.listbox.insert(tk.END, item.name)

    def main(self) -> str:
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()