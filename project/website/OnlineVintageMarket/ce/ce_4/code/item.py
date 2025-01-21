class Item:
    def __init__(self, name: str = '', description: str = '', price: float = 0.0) -> None:
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        with open('items.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

    def load_items(self) -> list:
        items_list = []
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items_list.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items_list