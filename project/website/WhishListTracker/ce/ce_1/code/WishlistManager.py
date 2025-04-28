class WishlistManager:
    def __init__(self, wishlist_file):
        self.wishlist_file = wishlist_file
        self.load_wishlist()

    def load_wishlist(self):
        self.wishlist = {}
        with open(self.wishlist_file, 'r') as file:
            for line in file:
                username, item_name, description, price = line.strip().split('|')
                if username not in self.wishlist:
                    self.wishlist[username] = []
                self.wishlist[username].append((item_name, description, float(price)))

    def add_item(self, username: str, item_name: str, description: str, price: float) -> bool:
        if username not in self.wishlist:
            self.wishlist[username] = []
        self.wishlist[username].append((item_name, description, price))
        with open(self.wishlist_file, 'a') as file:
            file.write(f"{username}|{item_name}|{description}|{price}\n")
        return True

    def view_wishlist(self, username: str) -> list:
        return self.wishlist.get(username, [])

    def remove_item(self, username: str, item_name: str) -> bool:
        if username in self.wishlist:
            self.wishlist[username] = [item for item in self.wishlist[username] if item[0] != item_name]
            self.save_wishlist()
            return True
        return False

    def save_wishlist(self):
        with open(self.wishlist_file, 'w') as file:
            for username, items in self.wishlist.items():
                for item_name, description, price in items:
                    file.write(f"{username}|{item_name}|{description}|{price}\n")