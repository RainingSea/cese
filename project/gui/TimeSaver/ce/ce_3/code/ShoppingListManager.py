import os
from ShoppingList import ShoppingList

class ShoppingListManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lists = {}
        self.load_lists()

    def create_list(self, name: str) -> None:
        if name not in self.lists:
            self.lists[name] = ShoppingList()
            self.save_lists()

    def delete_list(self, name: str) -> None:
        if name in self.lists:
            del self.lists[name]
            if os.path.exists(f"{name}.txt"):
                os.remove(f"{name}.txt")
            self.save_lists()

    def add_item(self, list_name: str, item: str, category: str) -> None:
        if list_name in self.lists:
            self.lists[list_name].add_item(item, category)
            self.save_lists()

    def view_lists(self) -> list:
        return list(self.lists.keys())

    def load_lists(self) -> None:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                for line in file:
                    list_name = line.strip()
                    self.lists[list_name] = ShoppingList()
                    self.load_items(list_name)

    def load_items(self, list_name: str) -> None:
        if os.path.exists(f"{list_name}.txt"):
            with open(f"{list_name}.txt", 'r') as file:
                for line in file:
                    category, item = line.strip().split(': ', 1)
                    self.lists[list_name].add_item(item, category)

    def save_lists(self) -> None:
        with open(self.file_path, 'w') as file:
            for list_name in self.lists:
                file.write(f"{list_name}\n")
                self.save_items(list_name)

    def save_items(self, list_name: str) -> None:
        with open(f"{list_name}.txt", 'w') as file:
            items = self.lists[list_name].get_items()
            for category, items_list in items.items():
                for item in items_list:
                    file.write(f"{category}: {item}\n")