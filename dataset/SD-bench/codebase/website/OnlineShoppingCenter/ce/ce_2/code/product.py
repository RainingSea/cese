class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    @staticmethod
    def load_products() -> list:
        products = []
        with open('products.txt', 'r') as file:
            for line in file:
                product_id, name, price = line.strip().split('|')
                products.append(Product(product_id, name, float(price)))
        return products