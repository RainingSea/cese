class PlayerTank:
    def __init__(self, position_x: int, position_y: int):
        self.health = 100
        self.position_x = position_x
        self.position_y = position_y

    def move(self, direction: str) -> None:
        if direction == 'up':
            self.position_y -= 5
        elif direction == 'down':
            self.position_y += 5
        elif direction == 'left':
            self.position_x -= 5
        elif direction == 'right':
            self.position_x += 5

    def fire(self) -> None:
        # Logic for firing a bullet would go here
        pass

    def take_damage(self, amount: int) -> None:
        self.health -= amount