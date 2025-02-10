class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save(self):
        with open('products.txt', 'a') as f:
            f.write(f"{self.name}|{self.description}|{self.price}\n")

    @staticmethod
    def load(name: str):
        with open('products.txt', 'r') as f:
            for line in f:
                product_data = line.strip().split('|')
                if product_data[0] == name:
                    return Product(product_data[0], product_data[1], float(product_data[2]))
        return None

class ProductManager:
    def __init__(self, products_file: str):
        self.products_file = products_file

    def add_product(self, user: User, name: str, description: str, price: float):
        product = Product(name, description, price)
        product.save()

    def get_products(self, user: User) -> list:
        products = []
        with open(self.products_file, 'r') as f:
            for line in f:
                product_data = line.strip().split('|')
                products.append(Product(product_data[0], product_data[1], float(product_data[2])))
        return products