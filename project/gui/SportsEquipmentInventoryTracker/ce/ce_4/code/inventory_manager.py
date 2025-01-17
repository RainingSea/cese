import json
from typing import List, Dict, Any

class InventoryManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.equipment = []
        self.load_data()

    def load_data(self) -> None:
        try:
            with open(self.file_path, 'r') as file:
                self.equipment = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.equipment = []

    def save_data(self) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(self.equipment, file, indent=4)

    def add_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        new_item = {
            "name": name,
            "quantity": quantity,
            "condition": condition,
            "location": location,
            "maintenance_alert": False
        }
        self.equipment.append(new_item)
        self.save_data()

    def update_equipment(self, name: str, quantity: int, condition: str, location: str) -> None:
        for item in self.equipment:
            if item["name"] == name:
                item["quantity"] = quantity
                item["condition"] = condition
                item["location"] = location
                self.save_data()
                return
        raise ValueError("Equipment not found.")

    def delete_equipment(self, name: str) -> None:
        self.equipment = [item for item in self.equipment if item["name"] != name]
        self.save_data()

    def search_equipment(self, query: str) -> List[Dict[str, Any]]:
        return [item for item in self.equipment if query.lower() in item["name"].lower()]

    def filter_equipment(self, condition: str, location: str) -> List[Dict[str, Any]]:
        return [
            item for item in self.equipment 
            if item["condition"] == condition and item["location"] == location
        ]