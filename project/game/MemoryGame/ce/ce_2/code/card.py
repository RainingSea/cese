class Card:
    def __init__(self, image: str) -> None:
        self.image = image
        self.is_flipped = False

    def flip(self) -> None:
        self.is_flipped = not self.is_flipped