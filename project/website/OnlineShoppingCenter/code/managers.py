import os

class UserManager:
    def __init__(self):
        self.users_file = 'users.txt'
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def validate_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    stored_user, stored_pass, email = line.strip().split('|')
                    if stored_user == username and stored_pass == password:
                        return True
        except FileNotFoundError:
            return False
        return False

    def register_user(self, username, password, email):
        if not username or not password or not email:
            return False
            
        with open(self.users_file, 'r') as f:
            for line in f:
                stored_user = line.strip().split('|')[0]
                if stored_user == username:
                    return False

        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}|{email}\n")
        return True

class ProductManager:
    def __init__(self):
        self.products_file = 'products.txt'
        if not os.path.exists(self.products_file):
            open(self.products_file, 'w').close()

    def get_products(self):
        products = []
        with open(self.products_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                products.append({
                    'id': parts[0],
                    'name': parts[1],
                    'price': parts[2],
                    'description': parts[3] if len(parts) > 3 else ''
                })
        return products

    def get_product(self, product_id):
        with open(self.products_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == product_id:
                    return {
                        'id': parts[0],
                        'name': parts[1],
                        'price': parts[2],
                        'description': parts[3] if len(parts) > 3 else ''
                    }
        return None

class CartManager:
    def __init__(self):
        self.carts_file = 'carts.txt'
        if not os.path.exists(self.carts_file):
            open(self.carts_file, 'w').close()

    def add_item(self, username, product_id):
        carts = {}
        with open(self.carts_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                carts[parts[0]] = parts[1].split(',') if parts[1] else []

        if username not in carts:
            carts[username] = []
        if product_id not in carts[username]:
            carts[username].append(product_id)

        with open(self.carts_file, 'w') as f:
            for user, items in carts.items():
                f.write(f"{user}|{','.join(items)}\n")

    def remove_item(self, username, product_id):
        carts = {}
        with open(self.carts_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                carts[parts[0]] = parts[1].split(',') if parts[1] else []

        if username in carts and product_id in carts[username]:
            carts[username].remove(product_id)

        with open(self.carts_file, 'w') as f:
            for user, items in carts.items():
                f.write(f"{user}|{','.join(items)}\n")

    def get_cart(self, username):
        with open(self.carts_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == username:
                    return parts[1].split(',') if parts[1] else []
        return []

    def clear_cart(self, username):
        carts = {}
        with open(self.carts_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] != username:
                    carts[parts[0]] = parts[1].split(',') if parts[1] else []

        with open(self.carts_file, 'w') as f:
            for user, items in carts.items():
                f.write(f"{user}|{','.join(items)}\n")

class OrderManager:
    def __init__(self):
        self.orders_file = 'orders.txt'
        if not os.path.exists(self.orders_file):
            open(self.orders_file, 'w').close()

    def create_order(self, username, product_ids, address, payment, total):
        import time
        order_id = str(int(time.time()))
        with open(self.orders_file, 'a') as f:
            f.write(f"{order_id}|{username}|{','.join(product_ids)}|{address}|{payment}|{total}\n")
        return order_id

    def get_order(self, order_id):
        with open(self.orders_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == order_id:
                    return {
                        'id': parts[0],
                        'username': parts[1],
                        'products': parts[2].split(','),
                        'address': parts[3],
                        'payment': parts[4],
                        'total': parts[5]
                    }
        return None