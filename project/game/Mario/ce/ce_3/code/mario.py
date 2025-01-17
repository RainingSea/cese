class Mario:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.velocity = 0

    def move(self, direction: str) -> None:
        if direction == 'left':
            self.x -= 5
        elif direction == 'right':
            self.x += 5

    def jump(self) -> None:
        self.velocity = -10

    def check_collision(self, obj) -> bool:
        return (self.x < obj.x + 30 and self.x + 50 > obj.x and
                self.y < obj.y + 30 and self.y + 50 > obj.y)