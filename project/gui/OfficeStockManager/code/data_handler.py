class Item:
    def __init__(self, name: str, category: str, quantity: int):
        self._name = name
        self._category = category
        self._quantity = int(quantity)

    def to_string(self) -> str:
        return f"{self._name},{self._category},{self._quantity}"