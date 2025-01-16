class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def add_item(self, name: str, description: str, price: float):
        item = Item(name, description, price)
        item.save()

    def load_items(self) -> list:
        items = []
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    def search_item(self, name: str) -> Item:
        items = self.load_items()
        for item in items:
            if item.name == name:
                return item
        return None