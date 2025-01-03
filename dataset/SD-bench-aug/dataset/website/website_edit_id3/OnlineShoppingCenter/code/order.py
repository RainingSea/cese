class Order:
    def __init__(self, user, cart, shipping_address: str, payment_info: str):
        self.user = user
        self.cart = cart
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save_order(self):
        with open('orders.txt', 'a') as file:
            file.write(f"{self.user.username}|{self.shipping_address}|{self.payment_info}|{self.cart.view_cart()}\n")