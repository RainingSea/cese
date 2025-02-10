import json

class OrderManager:
    def __init__(self, orders_file: str):
        self.orders_file = orders_file
        self.orders = self.load_orders()

    def create_order(self, user: str, cart: list) -> None:
        order = {'user': user, 'cart': cart}
        self.orders.append(order)
        self.save_orders()

    def load_orders(self) -> list:
        try:
            with open(self.orders_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_orders(self) -> None:
        with open(self.orders_file, 'w') as file:
            json.dump(self.orders, file)