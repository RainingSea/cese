class WishlistItem:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('wishlist.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_items() -> list:
        items = []
        try:
            with open('wishlist.txt', 'r') as file:
                for line in file:
                    name, description, price = line.strip().split('|')
                    items.append(WishlistItem(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items