import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager

class Main:
    def __init__(self):
        self.inventory_manager = InventoryManager('equipment_inventory.json')
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory")
        self.create_widgets()

    def create_widgets(self):
        self.equipment_listbox = tk.Listbox(self.root)
        self.equipment_listbox.pack()

        self.add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        self.add_button.pack()

        self.update_button = tk.Button(self.root, text="Update Equipment", command=self.update_equipment)
        self.update_button.pack()

        self.refresh_button = tk.Button(self.root, text="Refresh List", command=self.refresh_list)
        self.refresh_button.pack()

        self.refresh_list()

    def refresh_list(self):
        self.equipment_listbox.delete(0, tk.END)
        for equipment in self.inventory_manager.equipment_list:
            self.equipment_listbox.insert(tk.END, equipment.name)

    def add_equipment(self):
        # Here you would implement a dialog to collect equipment details
        equipment_data = {
            'name': 'Tennis Racket',
            'type': 'Racket',
            'quantity': 10,
            'condition': 'New',
            'availability': True,
            'location': 'Storage Room',
            'maintenance_alert': 'Check every 6 months'
        }
        self.inventory_manager.add_equipment(equipment_data)
        self.refresh_list()

    def update_equipment(self):
        selected_equipment = self.equipment_listbox.get(tk.ACTIVE)
        if selected_equipment:
            updated_info = {
                'condition': 'Used',
                'quantity': 8
            }
            self.inventory_manager.update_equipment(selected_equipment, updated_info)
            self.refresh_list()
        else:
            messagebox.showwarning("Update Error", "No equipment selected.")

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()