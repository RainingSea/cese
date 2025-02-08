from item import Item

class ShoppingListManager:
    def __init__(self, list_file: str, category_file: str) -> None:
        self.list_file = list_file
        self.category_file = category_file
        self.lists = {}
        self.load_lists()

    def create_list(self, name: str) -> None:
        if name not in self.lists:
            self.lists[name] = []

    def add_item(self, list_name: str, item: str, category: str) -> None:
        if list_name in self.lists:
            new_item = Item(item, category)
            self.lists[list_name].append(new_item)

    def import_items(self, list_name: str) -> list:
        if list_name in self.lists:
            return [(item.name, item.category) for item in self.lists[list_name]]
        return []

    def save_lists(self) -> None:
        with open(self.list_file, 'w') as f:
            for list_name, items in self.lists.items():
                item_strings = [f"{item.name}:{item.category}" for item in items]
                f.write(f"{list_name}|{','.join(item_strings)}\n")

    def load_lists(self) -> None:
        try:
            with open(self.list_file, 'r') as f:
                for line in f:
                    list_name, items_str = line.strip().split('|')
                    items = items_str.split(',')
                    self.lists[list_name] = [
                        Item(item.split(':')[0], item.split(':')[1]) for item in items
                    ]
        except FileNotFoundError:
            self.lists = {}