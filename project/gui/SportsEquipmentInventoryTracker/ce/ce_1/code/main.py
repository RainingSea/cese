import tkinter as tk
from tkinter import messagebox, simpledialog
from equipment_manager import EquipmentManager

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Equipment Inventory Tracker")
        self.equipment_manager = EquipmentManager()
        
        self.create_widgets()

    def create_widgets(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.equipment_listbox = tk.Listbox(self.root, width=50)
        self.equipment_listbox.pack(pady=10)

        self.load_equipment()

        add_menu = tk.Menu(self.menu_bar, tearoff=0)
        add_menu.add_command(label="Add Equipment", command=self.add_equipment)
        self.menu_bar.add_cascade(label="Add", menu=add_menu)

        update_menu = tk.Menu(self.menu_bar, tearoff=0)
        update_menu.add_command(label="Update Equipment", command=self.update_equipment)
        self.menu_bar.add_cascade(label="Update", menu=update_menu)

        search_menu = tk.Menu(self.menu_bar, tearoff=0)
        search_menu.add_command(label="Search Equipment", command=self.search_equipment)
        self.menu_bar.add_cascade(label="Search", menu=search_menu)

        filter_menu = tk.Menu(self.menu_bar, tearoff=0)
        filter_menu.add_command(label="Filter Equipment", command=self.filter_equipment)
        self.menu_bar.add_cascade(label="Filter", menu=filter_menu)

    def load_equipment(self):
        self.equipment_listbox.delete(0, tk.END)
        for equipment in self.equipment_manager.data:
            self.equipment_listbox.insert(tk.END, f"{equipment['type']} - {equipment['quantity']} - {equipment['condition']}")

    def add_equipment(self):
        equipment_type = simpledialog.askstring("Input", "Enter equipment type:")
        quantity = simpledialog.askinteger("Input", "Enter quantity:")
        condition = simpledialog.askstring("Input", "Enter condition:")
        availability = simpledialog.askstring("Input", "Enter availability:")
        location = simpledialog.askstring("Input", "Enter location:")
        
        if equipment_type and quantity is not None and condition and availability and location:
            self.equipment_manager.add_equipment({
                'type': equipment_type,
                'quantity': quantity,
                'condition': condition,
                'availability': availability,
                'location': location
            })
            self.load_equipment()
        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def update_equipment(self):
        index = simpledialog.askinteger("Input", "Enter equipment index to update:")
        if index is not None and 0 <= index < len(self.equipment_manager.data):
            updated_data = {}
            equipment_type = simpledialog.askstring("Input", "Enter new equipment type (leave blank for no change):")
            if equipment_type:
                updated_data['type'] = equipment_type
            
            quantity = simpledialog.askinteger("Input", "Enter new quantity (leave blank for no change):")
            if quantity is not None:
                updated_data['quantity'] = quantity
            
            condition = simpledialog.askstring("Input", "Enter new condition (leave blank for no change):")
            if condition:
                updated_data['condition'] = condition
            
            availability = simpledialog.askstring("Input", "Enter new availability (leave blank for no change):")
            if availability:
                updated_data['availability'] = availability
            
            location = simpledialog.askstring("Input", "Enter new location (leave blank for no change):")
            if location:
                updated_data['location'] = location
            
            self.equipment_manager.update_equipment(index, updated_data)
            self.load_equipment()
        else:
            messagebox.showwarning("Warning", "Invalid index!")

    def search_equipment(self):
        query = simpledialog.askstring("Input", "Enter search query:")
        if query:
            results = self.equipment_manager.search_equipment(query)
            self.equipment_listbox.delete(0, tk.END)
            for equipment in results:
                self.equipment_listbox.insert(tk.END, f"{equipment['type']} - {equipment['quantity']} - {equipment['condition']}")

    def filter_equipment(self):
        criteria = {}
        availability = simpledialog.askstring("Input", "Enter availability to filter (leave blank for no filter):")
        if availability:
            criteria['availability'] = availability
        
        location = simpledialog.askstring("Input", "Enter location to filter (leave blank for no filter):")
        if location:
            criteria['location'] = location
        
        results = self.equipment_manager.filter_equipment(criteria)
        self.equipment_listbox.delete(0, tk.END)
        for equipment in results:
            self.equipment_listbox.insert(tk.END, f"{equipment['type']} - {equipment['quantity']} - {equipment['condition']}")

def main():
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()