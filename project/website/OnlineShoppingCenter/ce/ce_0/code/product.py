class Product:
    def __init__(self, id: int, name: str, price: float, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    @staticmethod
    def load_products():
        products = []
        with open('products.txt', 'r') as file:
            for line in file.read().strip().split('\n'):
                id, name, price, description = line.split('|')
                products.append(Product(int(id), name, float(price), description))
        return products