class Tile:
    def __init__(self, value: int):
        self.value = value

    def combine(self, tile: 'Tile') -> None:
        if self.value == tile.value:
            self.value *= 2
            tile.value = 0  # Set the combined tile to 0