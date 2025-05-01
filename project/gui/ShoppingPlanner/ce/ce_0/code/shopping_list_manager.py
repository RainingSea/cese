class ShoppingListManager:
    def __init__(self):
        self.list_items = []
        self.categories = self.load_categories()

    def load_categories(self):
        categories = []
        if os.path.exists('categories.txt'):
            with open('categories.txt', 'r') as file:
                categories = [line.strip() for line in file.readlines()]
        return categories

    def create_list(self):
        self.list_items = []

    def add_item(self, item: str, category: str):
        if category in self.categories:
            self.list_items.append(f"{item}|{category}")
        else:
            raise ValueError("Category does not exist.")

    def import_items(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    item, category = line.strip().split('|')
                    self.add_item(item, category)
        else:
            raise FileNotFoundError("The specified file does not exist.")

    def get_items(self):
        return self.list_items