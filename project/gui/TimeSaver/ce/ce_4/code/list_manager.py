from data_storage import DataStorage

class ListManager:
    def __init__(self):
        self.shopping_lists = DataStorage.load_shopping_lists('shopping_lists.txt')
        self.items = DataStorage.load_items('items.txt')

    def create_list(self, name: str) -> None:
        if name not in self.shopping_lists:
            self.shopping_lists.append(name)
            self.save_data()

    def delete_list(self, name: str) -> None:
        if name in self.shopping_lists:
            self.shopping_lists.remove(name)
            if name in self.items:
                del self.items[name]
            self.save_data()

    def add_item(self, list_name: str, item: str, category: str) -> None:
        if list_name in self.shopping_lists:
            if list_name not in self.items:
                self.items[list_name] = []
            self.items[list_name].append((item, category))
            self.save_data()

    def edit_item(self, list_name: str, old_item: str, new_item: str) -> None:
        if list_name in self.items:
            for index, (item, category) in enumerate(self.items[list_name]):
                if item == old_item:
                    self.items[list_name][index] = (new_item, category)
                    self.save_data()
                    break

    def delete_item(self, list_name: str, item: str) -> None:
        if list_name in self.items:
            self.items[list_name] = [i for i in self.items[list_name] if i[0] != item]
            self.save_data()

    def set_reminder(self, list_name: str, reminder: str) -> None:
        # Reminder functionality can be implemented later
        pass

    def load_data(self) -> None:
        self.shopping_lists = DataStorage.load_shopping_lists('shopping_lists.txt')
        self.items = DataStorage.load_items('items.txt')

    def save_data(self) -> None:
        DataStorage.save_shopping_lists('shopping_lists.txt', self.shopping_lists)
        DataStorage.save_items('items.txt', self.items)