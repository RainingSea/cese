class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    @staticmethod
    def load_all() -> list:
        items = []
        try:
            with open('items.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    def save(self) -> None:
        with open('items.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")