class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product):
        if product.id in self.items:
            self.items[product.id]['quantity'] += 1
        else:
            self.items[product.id] = {'product': product, 'quantity': 1}

    def remove_item(self, product_id: int):
        if product_id in self.items:
            del self.items[product_id]

    def get_items(self):
        return self.items

    def clear(self):
        self.items.clear()