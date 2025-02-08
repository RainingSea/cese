class Score:
    def __init__(self):
        self.current_score = 0

    def update_score(self, points: int) -> None:
        """Updates the score by adding points."""
        self.current_score += points

    def get_score(self) -> int:
        """Returns the current score."""
        return self.current_score