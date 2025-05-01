class Score:
    def __init__(self) -> None:
        self.current_score = 0

    def update_score(self, points: int) -> None:
        self.current_score += points

    def get_score(self) -> int:
        return self.current_score