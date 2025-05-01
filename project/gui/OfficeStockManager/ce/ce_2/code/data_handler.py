import os

class DataHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def load_inventory(self):
        items = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    name, category, quantity, description = line.strip().split(',')
                    items.append(Item(name, category, int(quantity), description))
        return items

    def save_inventory(self, items):
        with open(self.filename, 'w') as file:
            for item in items:
                file.write(f"{item.name},{item.category},{item.quantity},{item.description}\n")