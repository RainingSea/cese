class ProductManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.products = self.load_products()

    def load_products(self) -> dict:
        products = {}
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    product_id, name, price = line.strip().split('|')
                    products[product_id] = {'name': name, 'price': price}
        except FileNotFoundError:
            pass
        return products

    def get_product_details(self, product_id: str) -> dict:
        return self.products.get(product_id, {})