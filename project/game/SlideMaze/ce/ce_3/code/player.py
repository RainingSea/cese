class Player:
    def __init__(self):
        self.position = (0, 0)
        self.score = 0

    def move(self, direction: str) -> None:
        # Placeholder for movement logic
        pass

    def collect_star(self) -> None:
        self.score += 1