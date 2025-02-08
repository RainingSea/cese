import os
from shopping_list import ShoppingList

class ShoppingListManager:
    def __init__(self):
        self.list_of_lists = {}

    def create_list(self, name: str) -> None:
        if name not in self.list_of_lists:
            self.list_of_lists[name] = ShoppingList(name)

    def delete_list(self, name: str) -> None:
        if name in self.list_of_lists:
            del self.list_of_lists[name]

    def edit_list(self, old_name: str, new_name: str) -> None:
        if old_name in self.list_of_lists:
            self.list_of_lists[new_name] = self.list_of_lists.pop(old_name)

    def load_lists(self) -> None:
        if os.path.exists('shopping_lists.txt'):
            with open('shopping_lists.txt', 'r') as file:
                for line in file:
                    list_name = line.strip()
                    self.create_list(list_name)

    def save_lists(self) -> None:
        with open('shopping_lists.txt', 'w') as file:
            for list_name in self.list_of_lists.keys():
                file.write(list_name + '\n')