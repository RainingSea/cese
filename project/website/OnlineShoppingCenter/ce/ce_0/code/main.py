import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.product_manager = ProductManager()
        self.cart_manager = CartManager()
        self.order_manager = OrderManager()

    def main(self):
        # Load data from files
        self.user_manager.load_users()
        self.product_manager.load_products()
        self.cart_manager.load_carts()
        self.order_manager.load_orders()
        
        # Start the web server (placeholder for actual web server code)
        print("Web server started. Navigate to the login page.")

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users.append({'username': username, 'password': password, 'email': email})

    def register(self, username: str, password: str, email: str) -> bool:
        self.users.append({'username': username, 'password': password, 'email': email})
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

class ProductManager:
    def __init__(self):
        self.products = []

    def load_products(self) -> list:
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, name, price = line.strip().split('|')
                    self.products.append({'product_id': product_id, 'name': name, 'price': float(price)})
        return self.products

class CartManager:
    def __init__(self):
        self.carts = {}

    def load_carts(self):
        if os.path.exists('cart.txt'):
            with open('cart.txt', 'r') as file:
                for line in file:
                    username, product_ids = line.strip().split('|')
                    self.carts[username] = product_ids.split(',')

    def add_to_cart(self, username: str, product_id: str) -> None:
        if username not in self.carts:
            self.carts[username] = []
        self.carts[username].append(product_id)
        self.save_cart(username)

    def remove_from_cart(self, username: str, product_id: str) -> None:
        if username in self.carts and product_id in self.carts[username]:
            self.carts[username].remove(product_id)
            self.save_cart(username)

    def view_cart(self, username: str) -> list:
        return self.carts.get(username, [])

    def save_cart(self, username: str) -> None:
        with open('cart.txt', 'w') as file:
            for user, product_ids in self.carts.items():
                file.write(f"{user}|{','.join(product_ids)}\n")

class OrderManager:
    def __init__(self):
        self.orders = []

    def load_orders(self):
        if os.path.exists('orders.txt'):
            with open('orders.txt', 'r') as file:
                for line in file:
                    username, product_ids, shipping_info, payment_info = line.strip().split('|')
                    self.orders.append({'username': username, 'product_ids': product_ids.split(','), 'shipping_info': shipping_info, 'payment_info': payment_info})

    def create_order(self, username: str, cart: list, shipping_info: str, payment_info: str) -> None:
        order_details = {
            'username': username,
            'product_ids': cart,
            'shipping_info': shipping_info,
            'payment_info': payment_info
        }
        self.orders.append(order_details)
        with open('orders.txt', 'a') as file:
            file.write(f"{username}|{','.join(cart)}|{shipping_info}|{payment_info}\n")

    def view_order_summary(self, order_id: str) -> str:
        if int(order_id) < len(self.orders):
            order = self.orders[int(order_id)]
            return f"Order Summary: {order}"
        return "Order not found."

if __name__ == "__main__":
    app = Main()
    app.main()