class Player:
    def __init__(self):
        self.level = 0
        self.score = 0

    def track_progress(self):
        # Logic to update and store player's current level and score
        with open('progress.txt', 'w') as file:
            file.write(f"{self.level}|{self.score}\n")

    def update_score(self, points: int):
        self.score += points
        self.track_progress()