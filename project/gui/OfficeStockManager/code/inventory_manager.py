import os
from typing import List
from data_handler import Item

class InventoryManager:
    def __init__(self, file_path: str = 'inventory.txt'):
        self._file_path = file_path
        self._items: List[Item] = self.load_inventory()

    def load_inventory(self) -> List[Item]:
        if not os.path.exists(self._file_path):
            return []
        with open(self._file_path, 'r') as file:
            return [Item(*line.strip().split(',')) for line in file.readlines()]

    def save_inventory(self) -> None:
        with open(self._file_path, 'w') as file:
            for item in self._items:
                file.write(item.to_string() + '\n')

    def add_item(self, item: Item) -> None:
        for existing_item in self._items:
            if existing_item._name == item._name:
                raise ValueError("Item already exists.")
        self._items.append(item)
        self.save_inventory()

    def update_quantity(self, name: str, quantity: int) -> None:
        for item in self._items:
            if item._name == name:
                item._quantity += quantity
                self.save_inventory()
                return
        raise ValueError("Item not found.")

    def search_item(self, name: str) -> Item:
        for item in self._items:
            if item._name == name:
                return item
        raise ValueError("Item not found.")

    def search_items(self, query: str) -> List[Item]:
        return [item for item in self._items if query.lower() in item._name.lower() or query.lower() in item._category.lower()]