import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self):
        self.inventory_manager = InventoryManager()
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory Tracker")
        self.setup_ui()

    def setup_ui(self):
        # Setup menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Setup buttons
        add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        add_button.pack()

        update_button = tk.Button(self.root, text="Update Equipment", command=self.update_equipment)
        update_button.pack()

        search_button = tk.Button(self.root, text="Search Equipment", command=self.search_equipment)
        search_button.pack()

        self.equipment_listbox = tk.Listbox(self.root)
        self.equipment_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_equipment()

    def load_equipment(self):
        self.equipment_listbox.delete(0, tk.END)
        for equipment in self.inventory_manager.equipment_list:
            self.equipment_listbox.insert(tk.END, f"{equipment.name} - {equipment.type} - {equipment.quantity}")

    def add_equipment(self):
        # This method would contain logic to add equipment
        pass

    def update_equipment(self):
        # This method would contain logic to update equipment
        pass

    def search_equipment(self):
        # This method would contain logic to search equipment
        pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()