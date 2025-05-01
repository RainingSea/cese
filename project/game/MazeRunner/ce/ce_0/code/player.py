class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction: str):
        if direction == "left":
            self.x -= 1
        elif direction == "right":
            self.x += 1
        elif direction == "up":
            self.y -= 1
        elif direction == "down":
            self.y += 1