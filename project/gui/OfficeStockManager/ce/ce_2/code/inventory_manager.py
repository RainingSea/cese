import json
from typing import List, Dict, Any

class InventoryManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.items = []
        self.load_items()

    def add_item(self, name: str, category: str, quantity: int) -> None:
        item = {'name': name, 'category': category, 'quantity': quantity}
        self.items.append(item)
        self.save_items()

    def update_item(self, name: str, quantity: int) -> None:
        for item in self.items:
            if item['name'] == name:
                item['quantity'] = quantity
                self.save_items()
                break

    def search_item(self, name: str) -> Dict[str, Any]:
        for item in self.items:
            if item['name'] == name:
                return item
        return {}

    def load_items(self) -> None:
        try:
            with open(self.filename, 'r') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            self.items = []

    def save_items(self) -> None:
        with open(self.filename, 'w') as file:
            json.dump(self.items, file, indent=4)