from item import Item

class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self):
        with open('items.txt', 'r') as file:
            for line in file:
                name, description, price = line.strip().split('|')
                self.add_item(name, description, float(price))

    def add_item(self, name: str, description: str, price: float):
        item = Item(name, description, price)
        self.items.append(item)

    def find_item(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None

    def get_all_items(self):
        return self.items