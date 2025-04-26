class CartManager:
    def __init__(self):
        self.cart = self.load_cart()

    def load_cart(self):
        cart = {}
        try:
            with open('cart.txt', 'r') as file:
                for line in file:
                    username, product_ids = line.strip().split('|')
                    cart[username] = product_ids.split(',')
        except FileNotFoundError:
            pass
        return cart

    def add_to_cart(self, username: str, product_id: str) -> None:
        if username not in self.cart:
            self.cart[username] = []
        self.cart[username].append(product_id)
        self.save_cart()

    def remove_from_cart(self, username: str, product_id: str) -> None:
        if username in self.cart and product_id in self.cart[username]:
            self.cart[username].remove(product_id)
            self.save_cart()

    def get_cart(self, username: str) -> list:
        return self.cart.get(username, [])

    def save_cart(self) -> None:
        with open('cart.txt', 'w') as file:
            for username, product_ids in self.cart.items():
                file.write(f"{username}|{','.join(product_ids)}\n")