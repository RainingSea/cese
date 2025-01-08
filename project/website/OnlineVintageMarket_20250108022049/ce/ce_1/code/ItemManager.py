import json

class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price
        }

class ItemManager:
    def __init__(self):
        self.items = self.load_items()

    def load_items(self) -> list:
        try:
            with open('items.txt', 'r') as file:
                return [Item(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_items(self) -> None:
        with open('items.txt', 'w') as file:
            for item in self.items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")

    def add_item(self, item: Item) -> None:
        self.items.append(item)
        self.save_items()

    def find_item(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None