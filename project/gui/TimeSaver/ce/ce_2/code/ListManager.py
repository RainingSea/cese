import os

class ListManager:
    def __init__(self):
        self.list = {}

    def create_list(self, name: str) -> None:
        if name not in self.list:
            self.list[name] = []
            self.save_lists()

    def delete_list(self, name: str) -> None:
        if name in self.list:
            del self.list[name]
            self.save_lists()

    def edit_list(self, old_name: str, new_name: str) -> None:
        if old_name in self.list and new_name not in self.list:
            self.list[new_name] = self.list.pop(old_name)
            self.save_lists()

    def load_lists(self) -> None:
        if os.path.exists('shopping_lists.txt'):
            with open('shopping_lists.txt', 'r') as file:
                for line in file:
                    name = line.strip()
                    self.list[name] = []

    def save_lists(self) -> None:
        with open('shopping_lists.txt', 'w') as file:
            for list_name in self.list.keys():
                file.write(f"{list_name}\n")