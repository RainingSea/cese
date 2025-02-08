from item import Item

class ShoppingList:
    def __init__(self, name: str) -> None:
        self.name = name
        self.items = []

    def add_item(self, item: str, category: str) -> None:
        new_item = Item(item, category)
        self.items.append(new_item)

    def remove_item(self, item: str) -> None:
        self.items = [i for i in self.items if i.name != item]