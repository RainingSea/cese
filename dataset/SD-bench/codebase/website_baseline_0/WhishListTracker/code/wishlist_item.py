class WishlistItem:
    """Represents an item in the wishlist."""
    
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        """Saves the wishlist item to a file."""
        with open('wishlist.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_items() -> list:
        """Loads wishlist items from a file."""
        items = []
        try:
            with open('wishlist.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items.append(WishlistItem(name, description, float(price)))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return items

    @staticmethod
    def remove_item(item_name: str) -> None:
        """Removes an item from the wishlist."""
        items = WishlistItem.load_items()
        items = [item for item in items if item.name != item_name]
        with open('wishlist.txt', 'w') as file:
            for item in items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")

    @staticmethod
    def update_item(item_name: str, new_description: str, new_price: float) -> None:
        """Updates an existing wishlist item."""
        items = WishlistItem.load_items()
        for item in items:
            if item.name == item_name:
                item.description = new_description
                item.price = new_price
        with open('wishlist.txt', 'w') as file:
            for item in items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")