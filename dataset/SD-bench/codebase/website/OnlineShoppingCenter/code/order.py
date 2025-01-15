class Order:
    def __init__(self, order_id: int, user: str, items: dict, shipping_address: str, payment_info: str):
        self.order_id = order_id
        self.user = user
        self.items = items
        self.shipping_address = shipping_address
        self.payment_info = payment_info

    def save(self) -> None:
        with open('orders.txt', 'a') as file:
            file.write(f"{self.order_id}|{self.user}|{self.items}|{self.shipping_address}|{self.payment_info}\n")

    @staticmethod
    def load_all() -> list:
        orders = []
        try:
            with open('orders.txt', 'r') as file:
                for line in file:
                    order_id, user, items, shipping_address, payment_info = line.strip().split('|')
                    orders.append(Order(int(order_id), user, eval(items), shipping_address, payment_info))
        except FileNotFoundError:
            pass
        return orders