class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        """Save item data (not used in this implementation)."""
        pass

    @staticmethod
    def load_all() -> list:
        """Load all items (not used in this implementation)."""
        pass

    @staticmethod
    def find_item(name: str) -> 'Item':
        """Find an item by name (not used in this implementation)."""
        pass