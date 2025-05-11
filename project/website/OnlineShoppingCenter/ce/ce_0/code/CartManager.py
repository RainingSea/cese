class CartManager:
    def __init__(self, cart_file: str):
        self.cart_file = cart_file

    def add_to_cart(self, username: str, product_id: str) -> bool:
        cart_items = self.load_cart(username)
        if product_id in cart_items:
            return False
        cart_items.append(product_id)
        self.save_cart(username, cart_items)
        return True

    def remove_from_cart(self, username: str, product_id: str) -> bool:
        cart_items = self.load_cart(username)
        if product_id in cart_items:
            cart_items.remove(product_id)
            self.save_cart(username, cart_items)
            return True
        return False

    def load_cart(self, username: str) -> list:
        try:
            with open(self.cart_file, 'r') as f:
                for line in f:
                    user, product_ids = line.strip().split('|')
                    if user == username:
                        return product_ids.split(',')
        except FileNotFoundError:
            pass
        return []

    def save_cart(self, username: str, cart_items: list) -> None:
        with open(self.cart_file, 'w') as f:
            f.write(f"{username}|{','.join(cart_items)}\n")