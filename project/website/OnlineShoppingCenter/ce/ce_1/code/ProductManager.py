class ProductManager:
    def __init__(self, filename):
        self.filename = filename
        self.products = []

    def load_products(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    product_id, name, description, price = line.strip().split('|')
                    self.products.append({
                        'id': product_id,
                        'name': name,
                        'description': description,
                        'price': float(price)
                    })
        except FileNotFoundError:
            pass

    def get_products(self):
        return self.products