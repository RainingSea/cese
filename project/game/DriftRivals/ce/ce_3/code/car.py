class Car:
    def __init__(self, model: str):
        self.model = model
        self.position_x = 0.0
        self.position_y = 0.0

    def move(self, direction: str):
        if direction == "left":
            self.position_x -= 1
        elif direction == "right":
            self.position_x += 1
        elif direction == "up":
            self.position_y -= 1
        elif direction == "down":
            self.position_y += 1

    def drift(self):
        # Logic for drifting
        pass