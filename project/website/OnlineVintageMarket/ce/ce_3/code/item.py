class Item:
    def __init__(self, item_name: str, description: str, price: float):
        self.item_name = item_name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.item_name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_items() -> list:
        items = []
        with open('items.txt', 'r') as file:
            for line in file:
                item_name, description, price = line.strip().split('|')
                items.append(Item(item_name, description, float(price)))
        return items