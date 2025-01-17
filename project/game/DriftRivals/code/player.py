class Player:
    def __init__(self):
        self.position = (0, 0)
        self.score = 0

    def move(self, direction: str) -> None:
        if direction == 'up':
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == 'down':
            self.position = (self.position[0], self.position[1] + 1)
        elif direction == 'left':
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == 'right':
            self.position = (self.position[0] + 1, self.position[1])
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    def drift(self) -> None:
        # Implement drift logic here
        self.position = (self.position[0] + 1, self.position[1] + 1)  # Example drift logic

    def calculate_score(self) -> int:
        return self.score