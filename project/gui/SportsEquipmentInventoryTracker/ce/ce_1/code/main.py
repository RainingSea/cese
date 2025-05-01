import json
import tkinter as tk
from tkinter import messagebox

class Equipment:
    def __init__(self, name: str, quantity: int, condition: str, location: str) -> None:
        self.name = name
        self.quantity = quantity
        self.condition = condition
        self.location = location

class Alert:
    def __init__(self, name: str, alert_type: str) -> None:
        self.name = name
        self.alert_type = alert_type

class InventoryManager:
    def __init__(self) -> None:
        self.equipment = self.load_equipment()
        self.alerts = self.load_alerts()

    def load_equipment(self) -> list:
        try:
            with open('equipment_data.json', 'r') as file:
                data = json.load(file)
                return [Equipment(**item) for item in data]
        except FileNotFoundError:
            return []

    def load_alerts(self) -> list:
        try:
            with open('alerts.json', 'r') as file:
                data = json.load(file)
                return [Alert(**item) for item in data]
        except FileNotFoundError:
            return []

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        new_equipment = Equipment(name, quantity, condition, location)
        self.equipment.append(new_equipment)
        self.save_equipment()

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        for item in self.equipment:
            if item.name == name:
                item.quantity = quantity
                item.condition = condition
                item.location = location
                self.save_equipment()
                return
        messagebox.showerror("Error", "Equipment not found.")

    def get_equipment(self) -> list:
        return self.equipment

    def set_alert(self, name: str, alert_type: str) -> None:
        new_alert = Alert(name, alert_type)
        self.alerts.append(new_alert)
        self.save_alerts()

    def get_alerts(self) -> list:
        return self.alerts

    def save_equipment(self) -> None:
        with open('equipment_data.json', 'w') as file:
            json.dump([vars(item) for item in self.equipment], file)

    def save_alerts(self) -> None:
        with open('alerts.json', 'w') as file:
            json.dump([vars(item) for item in self.alerts], file)

class Main:
    def __init__(self) -> None:
        self.inventory_manager = InventoryManager()
        self.root = tk.Tk()
        self.root.title("Sports Equipment Inventory")

        self.setup_ui()

    def setup_ui(self) -> None:
        # UI components setup goes here
        pass

    def main(self) -> str:
        self.root.mainloop()
        return "Application Closed"

if __name__ == "__main__":
    app = Main()
    app.main()