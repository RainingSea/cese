class Item:
    def __init__(self, item_id: int, name: str, description: str, price: float):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.item_id}|{self.name}|{self.description}|{self.price}\n")

class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self):
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    item_id, name, description, price = line.strip().split('|')
                    self.items.append(Item(int(item_id), name, description, float(price)))
        except FileNotFoundError:
            pass

    def create_listing(self, name: str, description: str, price: float):
        item_id = len(self.items) + 1
        new_item = Item(item_id, name, description, price)
        new_item.save()
        self.items.append(new_item)

    def search_item(self, name: str):
        return [item for item in self.items if name.lower() in item.name.lower()]

    def get_all_items(self):
        return self.items

    def get_item_by_id(self, item_id: int):
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None