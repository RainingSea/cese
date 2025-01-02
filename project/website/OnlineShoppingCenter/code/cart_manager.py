import json

class CartManager:
    def __init__(self, filename: str):
        self.filename = filename

    def add_to_cart(self, username: str, product_id: str) -> None:
        cart = self.load_cart(username)
        cart.append(product_id)
        self.save_cart(username, cart)

    def remove_from_cart(self, username: str, product_id: str) -> None:
        cart = self.load_cart(username)
        if product_id in cart:
            cart.remove(product_id)
            self.save_cart(username, cart)

    def load_cart(self, username: str) -> list:
        try:
            with open(self.filename, 'r') as file:
                carts = json.load(file)
                return carts.get(username, [])
        except FileNotFoundError:
            return []

    def save_cart(self, username: str, cart: list) -> None:
        try:
            with open(self.filename, 'r') as file:
                carts = json.load(file)
        except FileNotFoundError:
            carts = {}
        carts[username] = cart
        with open(self.filename, 'w') as file:
            json.dump(carts, file)