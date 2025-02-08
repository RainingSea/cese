class Card:
    def __init__(self, face: str):
        self.face = face
        self.is_flipped = False

    def flip(self) -> None:
        self.is_flipped = not self.is_flipped