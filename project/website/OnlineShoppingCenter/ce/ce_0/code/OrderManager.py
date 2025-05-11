class OrderManager:
    def __init__(self, orders_file: str):
        self.orders_file = orders_file

    def create_order(self, username: str, product_ids: list, shipping_address: str, payment_info: str) -> bool:
        with open(self.orders_file, 'a') as f:
            f.write(f"{username}|{','.join(product_ids)}|{shipping_address}|{payment_info}\n")
        return True