from user import User

class Order:
    def __init__(self, user: str, items: dict, shipping_address: str, payment_info: str):
        self.user = user
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save(self) -> None:
        with open('orders.txt', 'a') as file:
            file.write(f"{self.user}|{self.shipping_address}|{self.payment_info}|{self.items}\n")