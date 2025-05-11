class OrderManager:
    def __init__(self):
        self.orders = self.load_orders()

    def load_orders(self) -> list:
        try:
            with open('orders.txt', 'r') as file:
                return [line.strip().split('|') for line in file]
        except FileNotFoundError:
            return []

    def create_order(self, username: str, cart_items: list, shipping_info: dict):
        if not cart_items:
            raise ValueError("Cart is empty.")
        order_summary = f"User: {username} | Items: {', '.join(map(str, cart_items))} | Shipping: {shipping_info['address']} | Payment: {shipping_info['payment_method']}"
        self.orders.append(order_summary.split('|'))
        self.save_orders()

    def save_orders(self):
        with open('orders.txt', 'w') as file:
            for order in self.orders:
                file.write('|'.join(order) + '\n')

    def view_order(self, order_id: int) -> dict:
        if 0 <= order_id < len(self.orders):
            return self.orders[order_id]
        return {}