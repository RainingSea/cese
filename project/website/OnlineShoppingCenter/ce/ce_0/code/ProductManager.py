class ProductManager:
    def __init__(self, products_file):
        self.products_file = products_file

    def get_products(self):
        products = []
        try:
            with open(self.products_file, 'r') as file:
                for line in file:
                    product_data = line.strip().split(',')
                    products.append({
                        'id': int(product_data[0]),
                        'name': product_data[1],
                        'price': float(product_data[2]),
                        'description': product_data[3]
                    })
        except FileNotFoundError:
            pass
        return products