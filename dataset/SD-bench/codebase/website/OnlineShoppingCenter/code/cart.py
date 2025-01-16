class Cart:
    def __init__(self):
        self.items = {}

    def add_item(self, product_id: int) -> None:
        if product_id in self.items:
            self.items[product_id] += 1
        else:
            self.items[product_id] = 1

    def remove_item(self, product_id: int) -> None:
        if product_id in self.items:
            del self.items[product_id]

    def get_items(self) -> dict:
        return self.items

    def save(self) -> None:
        with open('cart.txt', 'w') as file:
            for product_id, quantity in self.items.items():
                file.write(f"{product_id}|{quantity}\n")