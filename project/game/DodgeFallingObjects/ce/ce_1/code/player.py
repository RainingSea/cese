class Player:
    def __init__(self, x: int):
        self.x_position = x
        self.width = 50
        self.height = 50

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.x_position -= 10
        elif direction == 'right':
            self.x_position += 10

    def get_position(self) -> tuple:
        return (self.x_position, 600 - self.height)  # Assuming the bottom of the screen is at y=600