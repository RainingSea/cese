import json
from typing import List
from item import Item

class InventoryManager:
    def __init__(self) -> None:
        self.items: List[Item] = []

    def add_item(self, name: str, category: str, quantity: int) -> None:
        new_item = Item(name, category, quantity)
        self.items.append(new_item)

    def update_item(self, name: str, quantity: int) -> None:
        for item in self.items:
            if item.name == name:
                item.quantity = quantity
                break

    def search_item(self, query: str) -> List[Item]:
        return [item for item in self.items if query.lower() in item.name.lower()]

    def load_inventory(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.items = [Item(**item) for item in data]
        except FileNotFoundError:
            self.items = []

    def save_inventory(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            json.dump([item.__dict__ for item in self.items], file)