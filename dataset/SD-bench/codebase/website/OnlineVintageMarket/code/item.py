class Item:
    """Item class to represent an item."""
    
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price