class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self) -> list:
        products = []
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    products.append(line.strip().split('|'))
        except FileNotFoundError:
            pass
        return products

    def get_product(self, product_id: int) -> dict:
        if 0 <= product_id < len(self.products):
            return {'id': product_id, 'name': self.products[product_id][0], 'price': self.products[product_id][1]}
        return {}