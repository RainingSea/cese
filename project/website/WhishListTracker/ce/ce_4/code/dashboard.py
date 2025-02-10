from wishlist_item import WishlistItem

class Dashboard:
    def add_item(self, name: str, description: str, price: float):
        item = WishlistItem(name, description, price)
        item.save()

    def update_item(self, name: str, description: str, price: float):
        items = WishlistItem.load_items()
        for item in items:
            if item.name == name:
                item.description = description
                item.price = price
                self.save_all(items)
                break

    def remove_item(self, name: str):
        items = WishlistItem.load_items()
        items = [item for item in items if item.name != name]
        self.save_all(items)

    def view_items(self) -> list:
        return WishlistItem.load_items()

    def save_all(self, items: list):
        with open('wishlist.txt', 'w') as file:
            for item in items:
                file.write(f"{item.name}|{item.description}|{item.price}\n")