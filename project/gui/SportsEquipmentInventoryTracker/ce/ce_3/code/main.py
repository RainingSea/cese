import tkinter as tk
from tkinter import messagebox
from inventory_manager import InventoryManager
from equipment import Equipment

class Main:
    def __init__(self):
        self.inventory_manager = InventoryManager()
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory Tracker")
        self.create_widgets()

    def create_widgets(self):
        # Create menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        # Add menu items
        inventory_menu = tk.Menu(menu)
        menu.add_cascade(label="Inventory", menu=inventory_menu)
        inventory_menu.add_command(label="Add Equipment", command=self.add_equipment)
        inventory_menu.add_command(label="Update Equipment", command=self.update_equipment)
        inventory_menu.add_command(label="Delete Equipment", command=self.delete_equipment)
        inventory_menu.add_command(label="Search Equipment", command=self.search_equipment)
        
        # Create inventory list
        self.inventory_listbox = tk.Listbox(self.root)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True)
        self.refresh_inventory_list()

    def refresh_inventory_list(self):
        self.inventory_listbox.delete(0, tk.END)
        for equipment in self.inventory_manager.equipment_list:
            self.inventory_listbox.insert(tk.END, f"{equipment.name} ({equipment.type}) - {equipment.quantity}")

    def add_equipment(self):
        # Simplified add equipment dialog
        self.show_equipment_dialog("Add Equipment", self.inventory_manager.add_equipment)

    def update_equipment(self):
        selected = self.inventory_listbox.curselection()
        if selected:
            equipment = self.inventory_manager.equipment_list[selected[0]]
            self.show_equipment_dialog("Update Equipment", self.inventory_manager.update_equipment, equipment)
        else:
            messagebox.showwarning("Update Equipment", "Please select an equipment item to update.")

    def delete_equipment(self):
        selected = self.inventory_listbox.curselection()
        if selected:
            equipment = self.inventory_manager.equipment_list[selected[0]]
            self.inventory_manager.delete_equipment(equipment.id)
            self.refresh_inventory_list()
        else:
            messagebox.showwarning("Delete Equipment", "Please select an equipment item to delete.")

    def search_equipment(self):
        query = tk.simpledialog.askstring("Search Equipment", "Enter equipment name to search:")
        if query:
            results = self.inventory_manager.search_equipment(query)
            self.inventory_listbox.delete(0, tk.END)
            for equipment in results:
                self.inventory_listbox.insert(tk.END, f"{equipment.name} ({equipment.type}) - {equipment.quantity}")

    def show_equipment_dialog(self, title: str, action, equipment: Equipment = None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        # Create input fields
        fields = ['ID', 'Name', 'Type', 'Quantity', 'Condition', 'Location', 'Maintenance Alert']
        entries = {}
        for field in fields:
            label = tk.Label(dialog, text=field)
            label.pack()
            entry = tk.Entry(dialog)
            entry.pack()
            entries[field] = entry
            if equipment:
                entry.insert(0, getattr(equipment, field.lower()))

        def submit():
            values = {field.lower(): entry.get() for field, entry in entries.items()}
            values['quantity'] = int(values['quantity'])  # Convert quantity to int
            action(Equipment(**values))
            dialog.destroy()
            self.refresh_inventory_list()

        submit_button = tk.Button(dialog, text="Submit", command=submit)
        submit_button.pack()

    def main(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.main()