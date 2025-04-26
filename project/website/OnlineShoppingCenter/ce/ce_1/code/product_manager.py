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