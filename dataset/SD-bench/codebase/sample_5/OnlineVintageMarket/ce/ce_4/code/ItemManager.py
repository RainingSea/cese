class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def to_string(self) -> str:
        return f"{self.name}|{self.description}|{self.price}"

class ItemManager:
    def __init__(self, items_file: str):
        self.items_file = items_file
        self.items = self.load_items()

    def add_item(self, item: Item) -> None:
        self.items.append(item)
        self.save_items()

    def load_items(self) -> list[Item]:
        items = []
        try:
            with open(self.items_file, 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    def save_items(self) -> None:
        with open(self.items_file, 'w') as file:
            for item in self.items:
                file.write(item.to_string() + '\n')

    def search_items(self, query: str) -> list[Item]:
        return [item for item in self.items if query.lower() in item.name.lower()]