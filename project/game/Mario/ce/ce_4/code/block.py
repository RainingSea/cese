from mushroom import Mushroom

class Block:
    def __init__(self, position: tuple):
        self.position = position

    def hit(self) -> Mushroom:
        return Mushroom(self.position)  # Releases a mushroom when hit