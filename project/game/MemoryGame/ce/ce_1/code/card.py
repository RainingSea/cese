class Card:
    def __init__(self, value: str):
        self.is_face_up = False
        self.value = value

    def flip(self) -> None:
        self.is_face_up = not self.is_face_up

    def is_match(self, other: 'Card') -> bool:
        return self.value == other.value