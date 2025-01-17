class Player:
    def __init__(self, x: int, width: int, height: int):
        self.x_position = x
        self.width = width
        self.height = height

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.x_position -= 5
        elif direction == 'right':
            self.x_position += 5

    def get_position(self) -> tuple:
        return (self.x_position, self.height)