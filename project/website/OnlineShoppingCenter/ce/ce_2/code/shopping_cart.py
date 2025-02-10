from product import Product

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id: str) -> None:
        self.items.append(product_id)

    def remove_item(self, product_id: str) -> None:
        if product_id in self.items:
            self.items.remove(product_id)

    def view_cart(self) -> list:
        return self.items