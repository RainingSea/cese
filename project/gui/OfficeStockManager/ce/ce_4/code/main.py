import tkinter as tk
from tkinter import messagebox, Listbox, Scrollbar
from inventory_manager import InventoryManager

class Main:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Office Stock Manager")
        self.inventory_manager = InventoryManager('inventory.json')

        self.create_widgets()

    def create_widgets(self) -> None:
        self.item_name_label = tk.Label(self.master, text="Item Name:")
        self.item_name_label.pack()

        self.item_name_entry = tk.Entry(self.master)
        self.item_name_entry.pack()

        self.category_label = tk.Label(self.master, text="Category:")
        self.category_label.pack()

        self.category_entry = tk.Entry(self.master)
        self.category_entry.pack()

        self.quantity_label = tk.Label(self.master, text="Quantity:")
        self.quantity_label.pack()

        self.quantity_entry = tk.Entry(self.master)
        self.quantity_entry.pack()

        self.add_button = tk.Button(self.master, text="Add Item", command=self.add_item)
        self.add_button.pack()

        self.update_button = tk.Button(self.master, text="Update Item", command=self.update_item)
        self.update_button.pack()

        self.search_label = tk.Label(self.master, text="Search Item:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.master)
        self.search_entry.pack()

        self.search_button = tk.Button(self.master, text="Search", command=self.search_item)
        self.search_button.pack()

        self.listbox = Listbox(self.master)
        self.listbox.pack()

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.load_inventory()

    def add_item(self) -> None:
        name = self.item_name_entry.get()
        category = self.category_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            self.inventory_manager.add_item(name, category, quantity)
            self.listbox.insert(tk.END, f"{name} - {category} - {quantity}")
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer.")

    def update_item(self) -> None:
        name = self.item_name_entry.get()
        try:
            quantity = int(self.quantity_entry.get())
            self.inventory_manager.update_item(name, quantity)
            self.load_inventory()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid Input", "Quantity must be an integer.")

    def search_item(self) -> None:
        name = self.search_entry.get()
        item = self.inventory_manager.search_item(name)
        if item:
            messagebox.showinfo("Item Found", f"Name: {item['name']}\nCategory: {item['category']}\nQuantity: {item['quantity']}")
        else:
            messagebox.showinfo("Item Not Found", "No item found with that name.")

    def load_inventory(self) -> None:
        self.listbox.delete(0, tk.END)
        for item in self.inventory_manager.inventory:
            self.listbox.insert(tk.END, f"{item['name']} - {item['category']} - {item['quantity']}")

    def clear_entries(self) -> None:
        self.item_name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

def main() -> str:
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()