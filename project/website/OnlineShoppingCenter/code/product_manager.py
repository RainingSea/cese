import json

class ProductManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.products = self.load_products()

    def load_products(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []