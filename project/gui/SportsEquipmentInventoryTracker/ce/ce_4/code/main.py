import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self):
        self.inventory_manager = InventoryManager("equipment.json")
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory Tracker")
        self.create_widgets()
        self.populate_equipment_list()

    def create_widgets(self):
        self.equipment_listbox = tk.Listbox(self.root, width=50)
        self.equipment_listbox.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(self.root, text="Update Equipment", command=self.update_equipment)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Equipment", command=self.delete_equipment)
        self.delete_button.pack(pady=5)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=10)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_equipment)
        self.search_button.pack(pady=5)

    def populate_equipment_list(self):
        self.equipment_listbox.delete(0, tk.END)
        for item in self.inventory_manager.equipment:
            self.equipment_listbox.insert(tk.END, f"{item['name']} - {item['quantity']} - {item['condition']} - {item['location']}")

    def add_equipment(self):
        # Sample data input
        name = "New Equipment"
        quantity = 10
        condition = "Good"
        location = "Storage Room"
        self.inventory_manager.add_equipment(name, quantity, condition, location)
        self.populate_equipment_list()

    def update_equipment(self):
        # Sample data input
        name = "New Equipment"
        quantity = 15
        condition = "Excellent"
        location = "Main Hall"
        try:
            self.inventory_manager.update_equipment(name, quantity, condition, location)
            self.populate_equipment_list()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def delete_equipment(self):
        name = "New Equipment"
        self.inventory_manager.delete_equipment(name)
        self.populate_equipment_list()

    def search_equipment(self):
        query = self.search_entry.get()
        results = self.inventory_manager.search_equipment(query)
        self.equipment_listbox.delete(0, tk.END)
        for item in results:
            self.equipment_listbox.insert(tk.END, f"{item['name']} - {item['quantity']} - {item['condition']} - {item['location']}")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()