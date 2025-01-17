from car import Car

class Player:
    def __init__(self):
        self.car = Car()
        self.score = 0.0

    def control(self, input: str) -> None:
        if input == "left":
            self.car.move("left")
        elif input == "right":
            self.car.move("right")
        elif input == "drift":
            self.car.drift()

    def calculate_score(self) -> float:
        # Placeholder for score calculation logic
        self.score += 10  # Increment score for demonstration
        return self.score