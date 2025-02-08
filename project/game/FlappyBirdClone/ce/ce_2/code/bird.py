class Bird:
    def __init__(self, y_position: float):
        self.y_position = y_position
        self.velocity = 0

    def flap(self):
        self.velocity = -10  # Flap moves the bird up

    def fall(self):
        self.velocity += 0.5  # Gravity effect
        self.y_position += self.velocity

    def get_position(self) -> float:
        return self.y_position