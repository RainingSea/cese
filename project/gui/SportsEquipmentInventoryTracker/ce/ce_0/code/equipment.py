class Equipment:
    def __init__(self, name: str, type: str, quantity: int, condition: str, location: str) -> None:
        self.name = name
        self.type = type
        self.quantity = quantity
        self.condition = condition
        self.location = location
        self.availability = quantity > 0