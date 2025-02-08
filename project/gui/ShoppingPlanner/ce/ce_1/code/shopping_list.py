class ShoppingList:
    def __init__(self):
        self.list_items = []

    def add_item(self, name: str, category: str) -> None:
        self.list_items.append((name, category))

    def import_items(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    name, category = line.strip().split(',')
                    self.add_item(name, category)
        except FileNotFoundError:
            print(f"File {file_path} not found.")

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            for name, category in self.list_items:
                file.write(f"{name},{category}\n")

    def get_items(self) -> list:
        return self.list_items