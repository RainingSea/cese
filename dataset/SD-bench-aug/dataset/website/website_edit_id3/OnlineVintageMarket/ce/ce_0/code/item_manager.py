class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self) -> None:
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    self.items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass

    def add_item(self, name: str, description: str, price: float) -> None:
        new_item = Item(name, description, price)
        new_item.save()
        self.items.append(new_item)

    def get_item(self, item_id: int) -> Item:
        return self.items[item_id] if 0 <= item_id < len(self.items) else None

    def search_items(self, query: str) -> list:
        return [item for item in self.items if query.lower() in item.name.lower()]