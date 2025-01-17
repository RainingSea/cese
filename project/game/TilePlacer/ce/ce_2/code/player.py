class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def update_score(self, points: int):
        self.score += points