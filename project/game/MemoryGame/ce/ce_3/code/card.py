class Card:
    def __init__(self, face: str):
        self.face = face
        self.is_flipped = False

    def flip(self):
        self.is_flipped = not self.is_flipped

    def is_match(self, other: 'Card') -> bool:
        return self.face == other.face