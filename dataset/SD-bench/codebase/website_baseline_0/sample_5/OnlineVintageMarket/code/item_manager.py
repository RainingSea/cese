from typing import List
from item import Item

class ItemManager:
    """Manage item data and operations."""
    
    def __init__(self):
        self.items: List[Item] = []

    def load_items(self) -> None:
        """Load items from a file."""
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.add_item(name, description, float(price))
        except FileNotFoundError:
            pass

    def save_items(self) -> None:
        """Save items to a file."""
        with open('items.txt', 'w') as file:
            for item in self.items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")

    def add_item(self, name: str, description: str, price: float) -> None:
        """Add a new item."""
        item = Item(name, description, price)
        self.items.append(item)
        self.save_items()

    def find_item(self, name: str) -> Item:
        """Find an item by name."""
        for item in self.items:
            if item.name == name:
                return item
        return None

    def search_items(self, query: str) -> List[Item]:
        """Search for items by query."""
        return [item for item in self.items if query.lower() in item.name.lower()]