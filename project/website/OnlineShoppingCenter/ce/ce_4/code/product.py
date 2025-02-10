import os

class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def load_from_file() -> list:
        products = []
        if os.path.exists('products.txt'):
            with open('products.txt', 'r') as f:
                for line in f:
                    id, name, price = line.strip().split('|')
                    products.append(Product(int(id), name, float(price)))
        return products