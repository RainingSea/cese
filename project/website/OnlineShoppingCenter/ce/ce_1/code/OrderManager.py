class OrderManager:
    def __init__(self, filename):
        self.filename = filename
        self.orders = []

    def create_order(self, username: str, product_ids: list, shipping_info: str) -> None:
        order_details = f"{username}|{','.join(product_ids)}|{shipping_info}\n"
        with open(self.filename, 'a') as file:
            file.write(order_details)

    def get_orders(self, username: str) -> list:
        user_orders = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    order_info = line.strip().split('|')
                    if order_info[0] == username:
                        user_orders.append(order_info)
        except FileNotFoundError:
            pass
        return user_orders