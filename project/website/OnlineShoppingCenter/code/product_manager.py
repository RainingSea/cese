class ProductManager:
    def __init__(self):
        self.products = []
        self.load_products()

    def load_products(self) -> None:
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, name, price, description = line.strip().split('|')
                    self.products.append({'product_id': product_id, 'name': name, 'price': float(price), 'description': description})
        except FileNotFoundError:
            pass

    def get_products(self) -> list:
        return self.products