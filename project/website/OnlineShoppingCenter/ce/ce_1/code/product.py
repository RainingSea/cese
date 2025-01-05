class Product:
    def __init__(self, id: int, name: str, price: float, description: str):
        self.id = id
        self.name = name
        self.price = price
        self.description = description

    @classmethod
    def load_products(cls) -> list:
        products_list = []
        with open('products.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')
                if len(data) == 4:
                    product = cls(int(data[0]), data[1], float(data[2]), data[3])
                    products_list.append(product)
        return products_list