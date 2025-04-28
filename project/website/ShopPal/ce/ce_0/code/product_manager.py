class ProductManager:
    def __init__(self):
        self.products = {}
        self.collections = {}

    def add_product(self, product_info: dict) -> None:
        self.products[product_info['id']] = product_info
        self.save_products()

    def track_price(self, product_id: str) -> None:
        # Price tracking logic would go here
        pass

    def search_products(self, query: str) -> list:
        return [product for product in self.products.values() if query in product['description']]

    def load_products(self) -> None:
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, description, reviews, price = line.strip().split(',')
                    self.products[product_id] = {
                        'description': description,
                        'reviews': reviews,
                        'price': price
                    }
        except FileNotFoundError:
            pass

    def save_products(self) -> None:
        with open('products.txt', 'w') as file:
            for product_id, info in self.products.items():
                file.write(f"{product_id},{info['description']},{info['reviews']},{info['price']}\n")

    def load_collections(self) -> None:
        try:
            with open('collections.txt', 'r') as file:
                for line in file:
                    username, *products = line.strip().split(',')
                    self.collections[username] = products
        except FileNotFoundError:
            pass

    def save_collections(self) -> None:
        with open('collections.txt', 'w') as file:
            for username, products in self.collections.items():
                file.write(f"{username},{','.join(products)}\n")