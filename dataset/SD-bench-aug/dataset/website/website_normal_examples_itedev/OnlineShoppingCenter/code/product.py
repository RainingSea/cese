class Product:
    def __init__(self, id: int, name: str, price: float):
        self.id = id
        self.name = name
        self.price = price

    def to_string(self) -> str:
        return f"{self.id}|{self.name}|{self.price}"