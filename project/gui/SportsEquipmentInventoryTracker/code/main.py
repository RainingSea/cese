import tkinter as tk
from tkinter import messagebox
from typing import List
import os
from datetime import datetime
import json

class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, location: str):
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.location = location

    def to_string(self) -> str:
        return f"{self.name}|{self.type}|{self.quantity}|{self.condition}|{self.location}"

    def get_condition(self) -> str:
        return self.condition

    def get_quantity(self) -> int:
        return self.quantity

    def get_location(self) -> str:
        return self.location

    def is_available(self) -> bool:
        return self.quantity > 0

class Alert:
    def __init__(self, id: int, equipment_name: str, message: str, date: str):
        self.id = id
        self.equipment_name = equipment_name
        self.message = message
        self.date = date

class AlertManager:
    def __init__(self):
        self.alerts = []
        self.load_alerts()

    def set_alert(self, equipment_name: str, message: str, date: str):
        alert_id = len(self.alerts) + 1
        new_alert = Alert(alert_id, equipment_name, message, date)
        self.alerts.append(new_alert)
        self.save_alerts()

    def view_alerts(self) -> List[Alert]:
        return self.alerts

    def remove_alert(self, alert_id: int):
        self.alerts = [alert for alert in self.alerts if alert.id != alert_id]
        self.save_alerts()

    def load_alerts(self):
        if os.path.exists('alerts.txt'):
            with open('alerts.txt', 'r') as file:
                for line in file:
                    id, equipment_name, message, date = line.strip().split('|')
                    self.alerts.append(Alert(int(id), equipment_name, message, date))

    def save_alerts(self):
        with open('alerts.txt', 'w') as file:
            for alert in self.alerts:
                file.write(f"{alert.id}|{alert.equipment_name}|{alert.message}|{alert.date}\n")

class InventoryManager:
    def __init__(self):
        self.equipment_list = []
        self.alert_manager = AlertManager()
        self.load_data()

    def add_equipment(self, name: str, type: str, quantity: int, condition: str, location: str):
        new_equipment = Equipment(name, type, quantity, condition, location)
        self.equipment_list.append(new_equipment)
        self.save_data()
        self.log_inventory_change("Added", new_equipment)

    def update_equipment(self, name: str, quantity: int, condition: str):
        for equipment in self.equipment_list:
            if equipment.name == name:
                equipment.quantity = quantity
                equipment.condition = condition
                self.save_data()
                self.log_inventory_change("Updated", equipment)
                return
        messagebox.showerror("Error", "Equipment not found.")

    def delete_equipment(self, name: str):
        self.equipment_list = [equipment for equipment in self.equipment_list if equipment.name != name]
        self.save_data()
        self.log_inventory_change("Deleted", Equipment(name, "", 0, "", ""))

    def search_equipment(self, query: str) -> List[Equipment]:
        return [equipment for equipment in self.equipment_list if query.lower() in equipment.name.lower()]

    def filter_equipment(self, criteria: dict) -> List[Equipment]:
        filtered_list = self.equipment_list
        for key, value in criteria.items():
            filtered_list = [equipment for equipment in filtered_list if getattr(equipment, key) == value]
        return filtered_list

    def load_data(self):
        if os.path.exists('equipment.txt'):
            with open('equipment.txt', 'r') as file:
                for line in file:
                    name, type, quantity, condition, location = line.strip().split('|')
                    self.equipment_list.append(Equipment(name, type, int(quantity), condition, location))

    def save_data(self):
        with open('equipment.txt', 'w') as file:
            for equipment in self.equipment_list:
                file.write(equipment.to_string() + '\n')

    def log_inventory_change(self, action: str, equipment: Equipment):
        with open('inventory_log.txt', 'a') as log_file:
            log_file.write(f"{self.get_current_date()}|{action}|{equipment.name}|{equipment.quantity}|{equipment.condition}|{equipment.location}\n")

    def get_current_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Equipment Inventory Tracker")
        self.manager = InventoryManager()
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.type_label = tk.Label(self.root, text="Type:")
        self.type_label.pack()
        self.type_entry = tk.Entry(self.root)
        self.type_entry.pack()

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.pack()
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.pack()

        self.condition_label = tk.Label(self.root, text="Condition:")
        self.condition_label.pack()
        self.condition_entry = tk.Entry(self.root)
        self.condition_entry.pack()

        self.location_label = tk.Label(self.root, text="Location:")
        self.location_label.pack()
        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Equipment", command=self.add_equipment)
        self.add_button.pack()

        self.alert_button = tk.Button(self.root, text="Manage Alerts", command=self.manage_alerts)
        self.alert_button.pack()

    def add_equipment(self):
        name = self.name_entry.get()
        type = self.type_entry.get()
        quantity = int(self.quantity_entry.get())
        condition = self.condition_entry.get()
        location = self.location_entry.get()
        self.manager.add_equipment(name, type, quantity, condition, location)
        messagebox.showinfo("Success", "Equipment added successfully.")
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.condition_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)

    def manage_alerts(self):
        alert_window = tk.Toplevel(self.root)
        alert_window.title("Manage Alerts")

        self.alert_name_label = tk.Label(alert_window, text="Equipment Name:")
        self.alert_name_label.pack()
        self.alert_name_entry = tk.Entry(alert_window)
        self.alert_name_entry.pack()

        self.alert_message_label = tk.Label(alert_window, text="Alert Message:")
        self.alert_message_label.pack()
        self.alert_message_entry = tk.Entry(alert_window)
        self.alert_message_entry.pack()

        self.alert_date_label = tk.Label(alert_window, text="Date (YYYY-MM-DD):")
        self.alert_date_label.pack()
        self.alert_date_entry = tk.Entry(alert_window)
        self.alert_date_entry.pack()

        self.set_alert_button = tk.Button(alert_window, text="Set Alert", command=self.set_alert)
        self.set_alert_button.pack()

        self.view_alerts_button = tk.Button(alert_window, text="View Alerts", command=self.view_alerts)
        self.view_alerts_button.pack()

    def set_alert(self):
        equipment_name = self.alert_name_entry.get()
        message = self.alert_message_entry.get()
        date = self.alert_date_entry.get()
        self.manager.alert_manager.set_alert(equipment_name, message, date)
        messagebox.showinfo("Success", "Alert set successfully.")

    def view_alerts(self):
        alerts = self.manager.alert_manager.view_alerts()
        alert_messages = "\n".join([f"{alert.id}: {alert.equipment_name} - {alert.message} on {alert.date}" for alert in alerts])
        messagebox.showinfo("Alerts", alert_messages if alert_messages else "No alerts available.")