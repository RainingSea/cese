import os

class Order:
    def __init__(self, user, products: list):
        self.user = user
        self.products = products

    def save_to_file(self):
        with open('orders.txt', 'a') as f:
            product_ids = ','.join(str(product.id) for product in self.products)
            f.write(f"{self.user.username}|{product_ids}\n")