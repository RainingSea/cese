class Item:
    def __init__(self, name: str, description: str, price: float) -> None:
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        with open('items.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def __init__(self) -> None:
        self.items = []

    def load_items(self) -> None:
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass

    def add_item(self, name: str, description: str, price: float) -> None:
        item = Item(name, description, price)
        item.save()
        self.items.append(item)

    def search_items(self, query: str) -> list:
        return [item for item in self.items if query.lower() in item.name.lower()]