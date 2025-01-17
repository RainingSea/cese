import json
from typing import List, Dict

class InventoryManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.inventory = self.load_inventory()

    def add_item(self, name: str, category: str, quantity: int) -> None:
        self.inventory.append({"name": name, "category": category, "quantity": quantity})
        self.save_inventory()

    def update_item(self, name: str, quantity: int) -> None:
        for item in self.inventory:
            if item['name'] == name:
                item['quantity'] = quantity
                break
        self.save_inventory()

    def search_item(self, name: str) -> Dict:
        for item in self.inventory:
            if item['name'] == name:
                return item
        return {}

    def load_inventory(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_inventory(self) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(self.inventory, file, indent=4)