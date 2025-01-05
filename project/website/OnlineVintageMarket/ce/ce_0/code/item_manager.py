class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def __init__(self):
        self.load_items()

    def add_item(self, name: str, description: str, price: float):
        item = Item(name, description, price)
        item.save()
        self.items[name] = item

    def load_items(self) -> list:
        self.items = {}
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.items[name] = Item(name, description, float(price))
        except FileNotFoundError:
            pass

    def search_item(self, name: str) -> Item:
        return self.items.get(name)