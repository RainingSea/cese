class Item:
    def __init__(self, item_id: int, name: str, description: str, price: float):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.item_id}|{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_items() -> list:
        items = []
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    item_id, name, description, price = line.strip().split('|')
                    items.append(Item(int(item_id), name, description, float(price)))
        except FileNotFoundError:
            pass  # Handle the case where the file does not exist
        return items