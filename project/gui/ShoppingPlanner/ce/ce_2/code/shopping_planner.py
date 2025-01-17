class ShoppingPlanner:
    def __init__(self):
        self.shopping_lists = {}
        self.categories = self.load_categories()

    def create_shopping_list(self, name: str):
        if name not in self.shopping_lists:
            self.shopping_lists[name] = []

    def add_item_to_list(self, list_name: str, item: str, category: str):
        if list_name in self.shopping_lists:
            categorized_item = f"{category}|{item}"
            self.shopping_lists[list_name].append(categorized_item)

    def import_items_from_list(self, list_name: str, source_list: str):
        if source_list in self.shopping_lists:
            self.shopping_lists[list_name].extend(self.shopping_lists[source_list])

    def save_list_to_file(self, list_name: str):
        with open('shopping_lists.txt', 'a') as file:
            for item in self.shopping_lists[list_name]:
                file.write(f"{list_name}|{item}\n")

    def load_lists_from_file(self):
        try:
            with open('shopping_lists.txt', 'r') as file:
                for line in file:
                    list_name, item = line.strip().split('|', 1)
                    if list_name not in self.shopping_lists:
                        self.shopping_lists[list_name] = []
                    self.shopping_lists[list_name].append(item)
        except FileNotFoundError:
            pass

    def load_categories(self):
        try:
            with open('categories.txt', 'r') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return []