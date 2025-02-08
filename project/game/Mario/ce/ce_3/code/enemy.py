class Enemy:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self) -> None:
        self.x -= 2  # Move left

    def check_collision(self, mario) -> bool:
        return (self.x < mario.x + 50 and self.x + 50 > mario.x and
                self.y < mario.y + 50 and self.y + 50 > mario.y)