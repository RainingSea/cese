class CartManager:
    def __init__(self):
        self.carts = self.load_cart()

    def load_cart(self) -> dict:
        try:
            carts = {}
            with open('cart.txt', 'r') as file:
                for line in file:
                    username, product_ids = line.strip().split('|')
                    carts[username] = list(map(int, product_ids.split(',')))
            return carts
        except FileNotFoundError:
            return {}

    def save_cart(self):
        with open('cart.txt', 'w') as file:
            for username, product_ids in self.carts.items():
                file.write(f"{username}|{','.join(map(str, product_ids))}\n")

    def add_to_cart(self, username: str, product_id: int):
        if username not in self.carts:
            self.carts[username] = []
        if product_id not in self.carts[username]:
            self.carts[username].append(product_id)
            self.save_cart()

    def remove_from_cart(self, username: str, product_id: int):
        if username in self.carts and product_id in self.carts[username]:
            self.carts[username].remove(product_id)
            self.save_cart()

    def view_cart(self, username: str) -> list:
        return self.carts.get(username, [])