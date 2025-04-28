import os

class WishlistManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_items()

    def load_items(self):
        self.items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    item_name, description, desired_price = line.strip().split('|')
                    self.items.append({
                        'item_name': item_name,
                        'description': description,
                        'desired_price': float(desired_price)
                    })

    def add_item(self, item_name: str, description: str, desired_price: float) -> bool:
        if any(item['item_name'] == item_name for item in self.items):
            return False
        self.items.append({
            'item_name': item_name,
            'description': description,
            'desired_price': desired_price
        })
        self.save_items()
        return True

    def view_items(self) -> list:
        return self.items

    def remove_item(self, item_name: str) -> bool:
        initial_length = len(self.items)
        self.items = [item for item in self.items if item['item_name'] != item_name]
        self.save_items()
        return len(self.items) < initial_length

    def save_items(self):
        with open(self.filename, 'w') as file:
            for item in self.items:
                file.write(f"{item['item_name']}|{item['description']}|{item['desired_price']}\n")