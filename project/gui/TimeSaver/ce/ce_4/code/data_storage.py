import os

class DataStorage:
    @staticmethod
    def load_shopping_lists(file_path: str) -> list:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    @staticmethod
    def save_shopping_lists(file_path: str, shopping_lists: list) -> None:
        with open(file_path, 'w') as file:
            for item in shopping_lists:
                file.write(f"{item}\n")

    @staticmethod
    def load_items(file_path: str) -> dict:
        items = {}
        if not os.path.exists(file_path):
            return items
        with open(file_path, 'r') as file:
            for line in file:
                list_name, item, category = line.strip().split('|')
                if list_name not in items:
                    items[list_name] = []
                items[list_name].append((item, category))
        return items

    @staticmethod
    def save_items(file_path: str, items: dict) -> None:
        with open(file_path, 'w') as file:
            for list_name, item_list in items.items():
                for item, category in item_list:
                    file.write(f"{list_name}|{item}|{category}\n")