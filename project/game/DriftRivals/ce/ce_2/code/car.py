class Car:
    def __init__(self):
        self.position = (0, 0)
        self.speed = 0.0

    def move(self, direction: str) -> None:
        if direction == "left":
            self.position = (self.position[0] - 5, self.position[1])
        elif direction == "right":
            self.position = (self.position[0] + 5, self.position[1])

    def drift(self) -> None:
        # Placeholder for drifting logic
        self.speed += 5.0  # Increase speed for demonstration