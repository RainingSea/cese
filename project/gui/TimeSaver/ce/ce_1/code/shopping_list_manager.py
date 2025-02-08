import os
from shopping_list import ShoppingList

class ShoppingListManager:
    def __init__(self):
        self.list_files = self.load_lists()

    def create_list(self, name: str) -> None:
        if name not in self.list_files:
            with open(f'shopping_lists/{name}.txt', 'w') as f:
                f.write('')
            self.list_files.append(name)

    def delete_list(self, name: str) -> None:
        if name in self.list_files:
            os.remove(f'shopping_lists/{name}.txt')
            self.list_files.remove(name)

    def load_lists(self) -> list:
        return [f[:-4] for f in os.listdir('shopping_lists/') if f.endswith('.txt')]

    def save_list(self, name: str, items: list) -> None:
        with open(f'shopping_lists/{name}.txt', 'w') as f:
            for item, category in items:
                f.write(f"{item},{category}\n")

    def load_list(self, name: str) -> list:
        items = []
        with open(f'shopping_lists/{name}.txt', 'r') as f:
            for line in f:
                item, category = line.strip().split(',')
                items.append((item, category))
        return items