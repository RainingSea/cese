import os

class InventoryManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.items = self.load_inventory()

    def load_inventory(self) -> list:
        """Loads the inventory from the text file into a list."""
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]

    def save_inventory(self, items: list) -> None:
        """Saves the current inventory list back to the text file."""
        with open(self.file_path, 'w') as file:
            for item in items:
                file.write(','.join(item) + '\n')

    def add_item(self, name: str, category: str, quantity: int) -> None:
        """Adds a new item to the inventory list and updates the text file."""
        self.items.append([name, category, str(quantity)])
        self.save_inventory(self.items)

    def update_item(self, name: str, quantity: int) -> None:
        """Updates the quantity of an existing item in the inventory list and updates the text file."""
        for item in self.items:
            if item[0] == name:
                item[2] = str(quantity)
                break
        self.save_inventory(self.items)

    def search_item(self, query: str) -> list:
        """Searches for items in the inventory based on a query and returns matching results."""
        return [item for item in self.items if query.lower() in item[0].lower() or query.lower() in item[1].lower()]