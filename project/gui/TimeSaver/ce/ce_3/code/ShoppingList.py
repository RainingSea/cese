class ShoppingList:
    def __init__(self):
        self.items = {}

    def add_item(self, item: str, category: str) -> None:
        if category not in self.items:
            self.items[category] = []
        self.items[category].append(item)

    def remove_item(self, item: str) -> None:
        for category in self.items:
            if item in self.items[category]:
                self.items[category].remove(item)
                break

    def get_items(self) -> dict:
        return self.items