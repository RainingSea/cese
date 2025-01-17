from shopping_list import ShoppingList

class ShoppingListManager:
    def __init__(self) -> None:
        self.lists = []

    def create_list(self, name: str) -> None:
        new_list = ShoppingList(name)
        self.lists.append(new_list)

    def add_item(self, list_name: str, item: str, category: str) -> None:
        for shopping_list in self.lists:
            if shopping_list.name == list_name:
                shopping_list.add_item(item, category)

    def import_list(self, file_name: str) -> None:
        with open(file_name, 'r') as file:
            for line in file:
                list_name, items = line.strip().split('|')
                new_list = ShoppingList(list_name)
                for item in items.split(','):
                    item_name, item_category = item.split(':')
                    new_list.add_item(item_name, item_category)
                self.lists.append(new_list)

    def save_lists(self) -> None:
        with open('shopping_lists.txt', 'w') as file:
            for shopping_list in self.lists:
                items_str = ','.join(f"{item.name}:{item.category}" for item in shopping_list.items)
                file.write(f"{shopping_list.name}|{items_str}\n")

    def load_lists(self) -> None:
        try:
            with open('shopping_lists.txt', 'r') as file:
                for line in file:
                    list_name, items = line.strip().split('|')
                    new_list = ShoppingList(list_name)
                    for item in items.split(','):
                        item_name, item_category = item.split(':')
                        new_list.add_item(item_name, item_category)
                    self.lists.append(new_list)
        except FileNotFoundError:
            pass