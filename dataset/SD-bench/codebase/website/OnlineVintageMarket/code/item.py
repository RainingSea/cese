class Item:
    def __init__(self, name='', description='', price=0.0):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('items.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

    def load_items(self):
        items = []
        try:
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items.append(Item(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

    def add_item(self, name, description, price):
        new_item = Item(name, description, price)
        new_item.save()

    def search_item(self, name):
        for item in self.load_items():
            if item.name == name:
                return item
        return None