class CartManager:
    def __init__(self, carts_file):
        self.carts_file = carts_file

    def add_item(self, user, product_id):
        carts = self._read_carts()
        if user in carts:
            if product_id not in carts[user]:
                carts[user].append(product_id)
        else:
            carts[user] = [product_id]
        self._write_carts(carts)

    def remove_item(self, user, product_id):
        carts = self._read_carts()
        if user in carts and product_id in carts[user]:
            carts[user].remove(product_id)
            self._write_carts(carts)

    def get_cart(self, user):
        carts = self._read_carts()
        return carts.get(user, [])

    def clear_cart(self, user):
        carts = self._read_carts()
        if user in carts:
            carts[user] = []
            self._write_carts(carts)

    def _read_carts(self):
        carts = {}
        try:
            with open(self.carts_file, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) > 1:
                        carts[parts[0]] = parts[1:]
        except FileNotFoundError:
            pass
        return carts

    def _write_carts(self, carts):
        with open(self.carts_file, 'w') as file:
            for user, items in carts.items():
                file.write(f"{user},{','.join(items)}\n")