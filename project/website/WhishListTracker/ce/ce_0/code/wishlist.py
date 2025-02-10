class WishlistItem:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self) -> None:
        with open('wishlist.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load_items() -> list:
        items = []
        try:
            with open('wishlist.txt', 'r') as f:
                for line in f:
                    name, description, price = line.strip().split('|')
                    items.append(WishlistItem(name, description, float(price)))
        except FileNotFoundError:
            pass
        return items

class WishlistController:
    def __init__(self):
        self.items = WishlistItem.load_items()

    def add_item(self, name: str, description: str, price: float) -> None:
        new_item = WishlistItem(name, description, price)
        new_item.save()
        self.items.append(new_item)

    def view_items(self) -> list:
        return self.items

    def update_item(self, name: str, description: str, price: float) -> None:
        for item in self.items:
            if item.name == name:
                item.description = description
                item.price = price
                self.save_all_items()
                break

    def remove_item(self, name: str) -> None:
        self.items = [item for item in self.items if item.name != name]
        self.save_all_items()

    def save_all_items(self) -> None:
        with open('wishlist.txt', 'w') as f:
            for item in self.items:
                f.write(f"{item.name}|{item.description}|{item.price}\n")