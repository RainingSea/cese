class ProductManager:
    def __init__(self, products_file: str):
        self.products_file = products_file

    def load_products(self) -> list:
        products = []
        try:
            with open(self.products_file, 'r') as f:
                for line in f:
                    product_id, name, price, description = line.strip().split('|')
                    products.append({
                        'id': product_id,
                        'name': name,
                        'price': price,
                        'description': description
                    })
        except FileNotFoundError:
            pass
        return products