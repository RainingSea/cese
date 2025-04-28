class ProductManager:
    def __init__(self):
        self.products = self.load_products()

    def load_products(self):
        products = []
        try:
            with open('products.txt', 'r') as file:
                for line in file:
                    product_id, name, price = line.strip().split('|')
                    products.append({'id': product_id, 'name': name, 'price': price})
        except FileNotFoundError:
            pass
        return products

    def search(self, query: str):
        return [product for product in self.products if query.lower() in product['name'].lower()]

    def get_product_details(self, product_id: str):
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None