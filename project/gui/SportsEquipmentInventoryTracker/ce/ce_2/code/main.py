import tkinter as tk
from tkinter import messagebox, Listbox, StringVar, IntVar, ttk
import os

class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, location: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.location = location

class Inventory:
    def __init__(self):
        self.equipment_list = []
        self.load_data()

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, location: str) -> None:
        new_equipment = Equipment(name, type, quantity, condition, location)
        self.equipment_list.append(new_equipment)
        self.save_data()

    def update_equipment(self, index: int, name: str, type: str, quantity: int, condition: str, location: str) -> None:
        if 0 <= index < len(self.equipment_list):
            self.equipment_list[index] = Equipment(name, type, quantity, condition, location)
            self.save_data()

    def search_equipment(self, query: str) -> list:
        return [equipment for equipment in self.equipment_list if query.lower() in equipment.name.lower()]

    def filter_equipment(self, type: str, condition: str) -> list:
        return [equipment for equipment in self.equipment_list if equipment.type == type and equipment.condition == condition]

    def load_data(self) -> None:
        if os.path.exists('equipment.txt'):
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type, quantity, condition, location = line.strip().split('|')
                    self.equipment_list.append(Equipment(name, type, int(quantity), condition, location))

    def save_data(self) -> None:
        with open('equipment.txt', 'w') as file:
            for equipment in self.equipment_list:
                file.write(f"{equipment.name}|{equipment.type}|{equipment.quantity}|{equipment.condition}|{equipment.location}\n")

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Equipment Inventory Tracker")
        self.inventory = Inventory()
        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Sports Equipment Inventory Tracker", font=("Arial", 16))
        self.title_label.pack()

        self.name_var = StringVar()
        self.type_var = StringVar()
        self.quantity_var = IntVar()
        self.condition_var = StringVar()
        self.location_var = StringVar()

        self.create_input_frame()
        self.create_listbox()
        self.create_buttons()

    def create_input_frame(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        tk.Label(input_frame, text="Name:").grid(row=0, column=0)
        tk.Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1)

        tk.Label(input_frame, text="Type:").grid(row=1, column=0)
        tk.Entry(input_frame, textvariable=self.type_var).grid(row=1, column=1)

        tk.Label(input_frame, text="Quantity:").grid(row=2, column=0)
        tk.Entry(input_frame, textvariable=self.quantity_var).grid(row=2, column=1)

        tk.Label(input_frame, text="Condition:").grid(row=3, column=0)
        tk.Entry(input_frame, textvariable=self.condition_var).grid(row=3, column=1)

        tk.Label(input_frame, text="Location:").grid(row=4, column=0)
        tk.Entry(input_frame, textvariable=self.location_var).grid(row=4, column=1)

    def create_listbox(self):
        self.listbox = Listbox(self.root)
        self.listbox.pack()
        self.update_listbox()

    def create_buttons(self):
        add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        add_button.pack()

        update_button = tk.Button(self.root, text="Update Equipment", command=self.update_equipment)
        update_button.pack()

    def add_equipment(self):
        name = self.name_var.get()
        type = self.type_var.get()
        quantity = self.quantity_var.get()
        condition = self.condition_var.get()
        location = self.location_var.get()
        self.inventory.add_equipment(name, type, quantity, condition, location)
        self.update_listbox()

    def update_equipment(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            name = self.name_var.get()
            type = self.type_var.get()
            quantity = self.quantity_var.get()
            condition = self.condition_var.get()
            location = self.location_var.get()
            self.inventory.update_equipment(index, name, type, quantity, condition, location)
            self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for equipment in self.inventory.equipment_list:
            self.listbox.insert(tk.END, f"{equipment.name} | {equipment.type} | {equipment.quantity} | {equipment.condition} | {equipment.location}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    app.run()