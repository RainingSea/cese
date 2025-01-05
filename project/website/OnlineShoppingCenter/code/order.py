class Order:
    def __init__(self, user, products):
        self.user = user
        self.products = products
        self.total = sum(product.price for product in products)

    def save_order(self):
        with open('orders.txt', 'a') as file:
            product_ids = ','.join(str(product.id) for product in self.products)
            file.write(f"{self.user.username}|{product_ids}|{self.total}\n")