class ShoppingList:
    def __init__(self, name: str):
        self.name = name
        self.items = []

    def add_item(self, item: str, category: str) -> None:
        self.items.append((item, category))

    def remove_item(self, item: str) -> None:
        self.items = [i for i in self.items if i[0] != item]

    def get_items(self) -> list:
        return self.items