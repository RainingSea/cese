from user import User  # Direct import from user.py
from product import Product  # Direct import from product.py

class Order:
    def __init__(self, user: User, products: list):
        self.user = user
        self.products = products
        self.total = sum(Product.load_products()[item].price for item in products)

    def save_order(self) -> None:
        with open('orders.txt', 'a') as file:
            product_ids = ','.join(map(str, self.products))
            file.write(f"{self.user.username}|{product_ids}|{self.total}\n")