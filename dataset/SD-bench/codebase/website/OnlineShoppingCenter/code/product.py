class Product:
    def __init__(self, id: int, name: str, price: float, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    @staticmethod
    def load_all() -> list:
        products = []
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    id, name, price, description = line.strip().split('|')
                    products.append(Product(int(id), name, float(price), description))
        except FileNotFoundError:
            pass
        return products