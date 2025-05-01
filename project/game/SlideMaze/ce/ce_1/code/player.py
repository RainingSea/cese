class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Score:
    def __init__(self):
        self.points = 0

class Player:
    def __init__(self):
        self.position = Position(0, 0)
        self.score = Score()

    def move(self, direction: str) -> None:
        if direction == "up":
            self.position.y -= 1
        elif direction == "down":
            self.position.y += 1
        elif direction == "left":
            self.position.x -= 1
        elif direction == "right":
            self.position.x += 1

    def collect_star(self) -> None:
        self.score.points += 1

    def reset(self) -> None:
        self.position = Position(0, 0)
        self.score = Score()