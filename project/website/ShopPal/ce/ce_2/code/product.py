class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price
        self.reviews = []

    def save(self):
        with open('products.txt', 'a') as file:
            file.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load(name: str):
        products = {}
        with open('products.txt', 'r') as file:
            for line in file:
                product_info = line.strip().split('|')
                products[product_info[0]] = Product(product_info[0], product_info[1], float(product_info[2]))
        return products.get(name)