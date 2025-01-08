import json

class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def to_dict(self) -> dict:
        return {"name": self.name, "description": self.description, "price": self.price}

class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self) -> list:
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.add_item(name, description, float(price))
        except FileNotFoundError:
            pass

    def save_items(self) -> None:
        with open('items.txt', 'w') as file:
            for item in self.items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")

    def add_item(self, name: str, description: str, price: float) -> None:
        item = Item(name, description, price)
        self.items.append(item)
        self.save_items()

    def find_item(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None