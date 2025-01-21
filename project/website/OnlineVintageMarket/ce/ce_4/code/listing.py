from item import Item

class Listing:
    def create_listing(self, name: str, description: str, price: float) -> None:
        new_item = Item(name, description, price)
        new_item.save()

    def view_items(self) -> list:
        return Item().load_items()

    def search_items(self, query: str) -> list:
        items = self.view_items()
        return [item for item in items if query.lower() in item.name.lower()]