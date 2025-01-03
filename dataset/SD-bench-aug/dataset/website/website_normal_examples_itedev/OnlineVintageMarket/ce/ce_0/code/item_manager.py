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
        self.items = []

    def add_item(self, item: Item) -> None:
        item.save()
        self.items.append(item)

    def get_items(self) -> list:
        return self.items

    def get_item_details(self, name: str) -> Item:
        for item in self.items:
            if item.name == name:
                return item
        return None

    def load_items(self):
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    self.items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass