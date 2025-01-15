class Collection:
    def __init__(self, user):
        self.user = user
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def save(self):
        with open('collections.txt', 'a') as file:
            product_names = ','.join([product.name for product in self.products])
            file.write(f"{self.user.username}|{product_names}\n")

    @staticmethod
    def load(user):
        collections = {}
        with open('collections.txt', 'r') as file:
            for line in file:
                username, product_names = line.strip().split('|')
                collections[username] = Collection(User(username, ''))
                collections[username].products = product_names.split(',')
        return collections.get(user.username)