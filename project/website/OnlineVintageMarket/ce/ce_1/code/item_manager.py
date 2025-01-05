class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def __init__(self):
        self.items = self.load_items()

    def add_item(self, name: str, description: str, price: float):
        item = Item(name, description, price)
        item.save()
        self.items.append(item)

    def load_items(self) -> list:
        items = []
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    def search_item(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None