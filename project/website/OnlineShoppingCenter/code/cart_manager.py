class CartManager:
    def __init__(self, username: str):
        self.username = username
        self.cart = self.load_cart()

    def load_cart(self) -> list:
        cart_items = []
        try:
            with open('carts.txt', 'r') as file:
                for line in file:
                    user, product_ids = line.strip().split('|')
                    if user == self.username:
                        cart_items = product_ids.split(',')
                        return cart_items
        except FileNotFoundError:
            pass
        return cart_items

    def add_to_cart(self, product_id: str) -> bool:
        if product_id not in self.cart:
            self.cart.append(product_id)
            self.save_cart()
            return True
        return False

    def remove_from_cart(self, product_id: str) -> None:
        if product_id in self.cart:
            self.cart.remove(product_id)
            self.save_cart()

    def get_cart(self) -> list:
        return self.cart

    def clear_cart(self) -> None:
        self.cart.clear()
        self.save_cart()

    def save_cart(self) -> None:
        with open('carts.txt', 'w') as file:
            file.write(f"{self.username}|{','.join(self.cart)}\n")