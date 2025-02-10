import os

class WishlistManager:
    def __init__(self, filename):
        self.filename = filename

    def add_item(self, username: str, item_name: str, description: str, price: float) -> bool:
        user_file = f"{self.filename}{username}.txt"
        with open(user_file, 'a') as file:
            file.write(f"{item_name},{description},{price}\n")
        return True

    def view_wishlist(self, username: str) -> list:
        user_file = f"{self.filename}{username}.txt"
        if not os.path.exists(user_file):
            return []
        with open(user_file, 'r') as file:
            return [line.strip().split(',') for line in file]

    def update_item(self, username: str, item_name: str, new_description: str, new_price: float) -> bool:
        user_file = f"{self.filename}{username}.txt"
        items = self.load_wishlist(username)
        for index, item in enumerate(items):
            if item[0] == item_name:
                items[index] = [item_name, new_description, str(new_price)]
                break
        self.save_wishlist(username, items)
        return True

    def remove_item(self, username: str, item_name: str) -> bool:
        items = self.load_wishlist(username)
        items = [item for item in items if item[0] != item_name]
        self.save_wishlist(username, items)
        return True

    def load_wishlist(self, username: str) -> list:
        user_file = f"{self.filename}{username}.txt"
        if not os.path.exists(user_file):
            return []
        with open(user_file, 'r') as file:
            return [line.strip().split(',') for line in file]

    def save_wishlist(self, username: str, items: list) -> None:
        user_file = f"{self.filename}{username}.txt"
        with open(user_file, 'w') as file:
            for item in items:
                file.write(','.join(item) + '\n')