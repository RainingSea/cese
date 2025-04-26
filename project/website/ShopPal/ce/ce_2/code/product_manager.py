class ProductManager:
    def __init__(self):
        self.products = self.load_products()
        self.collections = self.load_collections()

    def load_products(self):
        products = []
        with open('products.txt', 'r') as file:
            for line in file:
                id_, name, description, price = line.strip().split('|')
                products.append({'id': id_, 'name': name, 'description': description, 'price': float(price)})
        return products

    def load_collections(self):
        collections = []
        with open('collections.txt', 'r') as file:
            for line in file:
                collections.append(line.strip().split('|'))
        return collections

    def add_product(self, name: str, description: str, price: float) -> None:
        product_id = str(len(self.products) + 1)
        self.products.append({'id': product_id, 'name': name, 'description': description, 'price': price})
        with open('products.txt', 'a') as file:
            file.write(f"{product_id}|{name}|{description}|{price}\n")

    def track_price(self, product_id: str) -> None:
        # This method can be expanded to track price changes.
        pass

    def search_products(self, query: str):
        return [product for product in self.products if query.lower() in product['name'].lower()]