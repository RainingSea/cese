import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Main:
    def __init__(self):
        self.inventory = Inventory()
        self.inventory.load_data()
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory Tracker")
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Create input fields
        self.name_entry = tk.Entry(self.root)
        self.type_entry = tk.Entry(self.root)
        self.quantity_entry = tk.Entry(self.root)
        self.condition_entry = tk.Entry(self.root)
        self.availability_var = tk.BooleanVar()
        self.availability_check = tk.Checkbutton(self.root, text="Available", variable=self.availability_var)
        self.location_entry = tk.Entry(self.root)

        # Create buttons
        self.add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        self.update_button = tk.Button(self.root, text="Update Equipment", command=self.update_equipment)
        self.search_button = tk.Button(self.root, text="Search Equipment", command=self.search_equipment)
        self.filter_button = tk.Button(self.root, text="Filter Equipment", command=self.filter_equipment)

        # Create listbox
        self.equipment_listbox = tk.Listbox(self.root)
        self.equipment_listbox.bind('<<ListboxSelect>>', self.on_select)

        # Layout
        self.name_entry.pack()
        self.type_entry.pack()
        self.quantity_entry.pack()
        self.condition_entry.pack()
        self.availability_check.pack()
        self.location_entry.pack()
        self.add_button.pack()
        self.update_button.pack()
        self.search_button.pack()
        self.filter_button.pack()
        self.equipment_listbox.pack()

    def add_equipment(self):
        equipment = Equipment(
            self.name_entry.get(),
            self.type_entry.get(),
            int(self.quantity_entry.get()),
            self.condition_entry.get(),
            self.availability_var.get(),
            self.location_entry.get()
        )
        self.inventory.add_equipment(equipment)
        self.update_listbox()

    def update_equipment(self):
        selected_item = self.equipment_listbox.curselection()
        if selected_item:
            equipment = Equipment(
                self.name_entry.get(),
                self.type_entry.get(),
                int(self.quantity_entry.get()),
                self.condition_entry.get(),
                self.availability_var.get(),
                self.location_entry.get()
            )
            self.inventory.update_equipment(equipment)
            self.update_listbox()

    def search_equipment(self):
        query = simpledialog.askstring("Search", "Enter equipment name to search:")
        results = self.inventory.search_equipment(query)
        self.update_listbox(results)

    def filter_equipment(self):
        criteria = {
            "type": simpledialog.askstring("Filter", "Enter equipment type to filter:"),
            "availability": self.availability_var.get()
        }
        results = self.inventory.filter_equipment(criteria)
        self.update_listbox(results)

    def update_listbox(self, equipment_list=None):
        self.equipment_listbox.delete(0, tk.END)
        if equipment_list is None:
            equipment_list = self.inventory.equipment_list
        for equipment in equipment_list:
            self.equipment_listbox.insert(tk.END, equipment.name)

    def on_select(self, event):
        selected_index = self.equipment_listbox.curselection()
        if selected_index:
            equipment = self.inventory.equipment_list[selected_index[0]]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, equipment.name)
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(0, equipment.type)
            self.quantity_entry.delete(0, tk.END)
            self.quantity_entry.insert(0, equipment.quantity)
            self.condition_entry.delete(0, tk.END)
            self.condition_entry.insert(0, equipment.condition)
            self.availability_var.set(equipment.availability)
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, equipment.location)

class Inventory:
    def __init__(self):
        self.equipment_list = []

    def add_equipment(self, equipment):
        self.equipment_list.append(equipment)
        self.save_data()

    def update_equipment(self, equipment):
        for i, item in enumerate(self.equipment_list):
            if item.name == equipment.name:
                self.equipment_list[i] = equipment
                self.save_data()
                break

    def search_equipment(self, query):
        return [item for item in self.equipment_list if query.lower() in item.name.lower()]

    def filter_equipment(self, criteria):
        return [item for item in self.equipment_list if item.type == criteria["type"] and item.availability == criteria["availability"]]

    def load_data(self):
        try:
            with open('equipment.json', 'r') as file:
                self.equipment_list = [Equipment(**data) for data in json.load(file)]
        except FileNotFoundError:
            self.equipment_list = []

    def save_data(self):
        with open('equipment.json', 'w') as file:
            json.dump([equipment.__dict__ for equipment in self.equipment_list], file)

class Equipment:
    def __init__(self, name, type, quantity, condition, availability, location):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.availability = availability
        self.location = location

class Alert:
    def __init__(self, equipment_name, alert_type, alert_date):
        self.equipment_name = equipment_name
        self.alert_type = alert_type
        self.alert_date = alert_date

if __name__ == "__main__":
    Main()