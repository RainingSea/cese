class OrderManager:
    def __init__(self):
        self.orders = []
        self.load_orders()

    def create_order(self, username: str, cart: list, shipping_address: str, payment_info: str) -> None:
        if not cart:
            raise ValueError("Cart is empty.")
        order_id = len(self.orders) + 1
        self.orders.append({'order_id': order_id, 'username': username, 'cart': cart, 'shipping_address': shipping_address, 'payment_info': payment_info})
        self.save_orders()

    def load_orders(self) -> None:
        try:
            with open('orders.txt', 'r') as file:
                for line in file:
                    order_id, username, cart, shipping_address, payment_info = line.strip().split('|')
                    self.orders.append({'order_id': int(order_id), 'username': username, 'cart': cart.split(','), 'shipping_address': shipping_address, 'payment_info': payment_info})
        except FileNotFoundError:
            pass

    def save_orders(self) -> None:
        with open('orders.txt', 'w') as file:
            for order in self.orders:
                file.write(f"{order['order_id']}|{order['username']}|{','.join(order['cart'])}|{order['shipping_address']}|{order['payment_info']}\n")