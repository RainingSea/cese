class Collection:
    def __init__(self, user: str):
        self.user = user
        self.products = []

    def add_product(self, product: str) -> None:
        self.products.append(product)
        self.save()

    def load(self) -> list:
        try:
            with open('collections.txt', 'r') as file:
                for line in file:
                    user, product = line.strip().split('|')
                    if user == self.user:
                        self.products.append(product)
        except FileNotFoundError:
            pass
        return self.products

    def save(self) -> None:
        with open('collections.txt', 'a') as file:
            for product in self.products:
                file.write(f"{self.user}|{product}\n")