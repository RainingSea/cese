class ItemManager:
    def __init__(self):
        self.items = []

    def load_items(self):
        if os.path.exists('items.txt'):
            with open('items.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    self.items.append((name, description, float(price)))

    def add_item(self, name: str, description: str, price: float) -> bool:
        self.items.append((name, description, price))
        with open('items.txt', 'a') as file:
            file.write(f"{name}|{description}|{price}\n")
        return True

    def get_items(self) -> list:
        return self.items

    def get_item_details(self, name: str) -> str:
        for item in self.items:
            if item[0] == name:
                return f"Name: {item[0]}, Description: {item[1]}, Price: {item[2]}"
        return "Item not found."