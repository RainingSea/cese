class Listing:
    def __init__(self, items):
        self.items = items

    def create_listing(self, item):
        item.save()
        self.items.append(item)

    def view_items(self):
        return self.items

    def search_item(self, name: str):
        for item in self.items:
            if item.name == name:
                return item
        return None