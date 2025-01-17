import os

class InventoryManager:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.inventory = self.load_inventory()

    def add_item(self, item_name: str, item_type: str, quantity: int) -> None:
        self.inventory.append({'item_name': item_name, 'item_type': item_type, 'quantity': quantity})
        self.save_inventory()

    def update_quantity(self, item_name: str, quantity: int) -> None:
        for item in self.inventory:
            if item['item_name'] == item_name:
                item['quantity'] = quantity
                break
        self.save_inventory()

    def search_item(self, item_name: str) -> dict:
        for item in self.inventory:
            if item['item_name'] == item_name:
                return item
        return {}

    def load_inventory(self) -> list:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            items = []
            for line in file:
                item_name, item_type, quantity = line.strip().split(',')
                items.append({'item_name': item_name, 'item_type': item_type, 'quantity': int(quantity)})
            return items

    def save_inventory(self) -> None:
        with open(self.file_path, 'w') as file:
            for item in self.inventory:
                file.write(f"{item['item_name']},{item['item_type']},{item['quantity']}\n")