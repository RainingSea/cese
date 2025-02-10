from shopping_cart import ShoppingCart

class Checkout:
    def __init__(self, shipping_address: str, payment_info: str):
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def process_order(self, cart: ShoppingCart) -> None:
        # Here you would normally process the order
        pass