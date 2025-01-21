class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_all():
        items = []
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    @staticmethod
    def get_item_details(name: str):
        items = Item.load_all()
        for item in items:
            if item.name == name:
                return item
        return None