from item import Item
from data_handler import DataHandler

class InventoryManager:
    def __init__(self):
        self.items = []
        self.data_handler = DataHandler('inventory.txt')
        self.load_inventory()

    def add_item(self, name: str, category: str, quantity: int, description: str):
        new_item = Item(name, category, quantity, description)
        self.items.append(new_item)
        self.save_inventory()

    def update_quantity(self, name: str, quantity: int):
        for item in self.items:
            if item.name == name:
                item.quantity += quantity
                self.save_inventory()
                return

    def search_item(self, name: str):
        for item in self.items:
            if item.name == name:
                return item
        return None

    def load_inventory(self):
        self.items = self.data_handler.load_inventory()

    def save_inventory(self):
        self.data_handler.save_inventory(self.items)