class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, word: str) -> int:
        return len(word)  # Simple scoring based on word length