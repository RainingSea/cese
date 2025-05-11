class CartManager:
    def __init__(self, filename):
        self.filename = filename
        self.carts = {}

    def load_cart(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    username, product_ids = line.strip().split('|')
                    self.carts[username] = product_ids.split(',')
        except FileNotFoundError:
            pass

    def add_to_cart(self, username: str, product_id: str) -> None:
        if username not in self.carts:
            self.carts[username] = []
        if product_id not in self.carts[username]:
            self.carts[username].append(product_id)
            self.save_cart()

    def remove_from_cart(self, username: str, product_id: str) -> None:
        if username in self.carts and product_id in self.carts[username]:
            self.carts[username].remove(product_id)
            self.save_cart()

    def get_cart(self, username: str) -> list:
        return self.carts.get(username, [])

    def save_cart(self):
        with open(self.filename, 'w') as file:
            for username, product_ids in self.carts.items():
                file.write(f"{username}|{','.join(product_ids)}\n")