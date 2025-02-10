from item import Item

class Listing:
    def __init__(self):
        self.items = self.load_items()

    def create_listing(self, name: str, description: str, price: float) -> None:
        new_item = Item(name, description, price)
        new_item.save()
        self.items.append(new_item)

    def view_listings(self) -> list:
        return self.items

    def load_items(self) -> list:
        items = []
        with open('items.txt', 'r') as file:
            for line in file:
                name, description, price = line.strip().split('|')
                items.append(Item(name, description, float(price)))
        return items