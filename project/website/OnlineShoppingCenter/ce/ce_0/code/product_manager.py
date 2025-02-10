import json

class ProductManager:
    def __init__(self, products_file: str):
        self.products_file = products_file
        self.products = self.load_products()

    def load_products(self) -> list:
        try:
            with open(self.products_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def get_product_list(self) -> list:
        return self.products