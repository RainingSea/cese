class Block:
    def __init__(self, color: str, position: tuple):
        self.color = color
        self.position = position

    def is_adjacent(self, other: 'Block') -> bool:
        return (abs(self.position[0] - other.position[0]) == 1 and self.position[1] == other.position[1]) or \
               (self.position[0] == other.position[0] and abs(self.position[1] - other.position[1]) == 1)

    def draw(self):
        # Logic to draw the block on the screen
        print(f"Drawing block at {self.position} with color {self.color}")