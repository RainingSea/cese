class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, time: float, stars_collected: int, moves: int) -> int:
        self.points = (stars_collected * 10) - (time * 2) - (moves * 1)
        return self.points

    def save_score(self, file: str) -> None:
        with open(file, 'a') as f:
            f.write(f"player|{self.points}\n")