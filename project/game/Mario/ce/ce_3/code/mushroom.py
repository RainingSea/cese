class Mushroom:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def fall(self) -> None:
        self.y += 5  # Simple gravity effect

    def check_collision(self, mario) -> bool:
        return (self.x < mario.x + 50 and self.x + 30 > mario.x and
                self.y < mario.y + 50 and self.y + 30 > mario.y)