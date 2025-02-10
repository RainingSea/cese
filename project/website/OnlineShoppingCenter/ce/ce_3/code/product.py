class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    @staticmethod
    def load_products():
        products = []
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    id, name, price = line.strip().split('|')
                    products.append(Product(int(id), name, float(price)))
        except FileNotFoundError:
            pass
        return products