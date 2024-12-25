class Score:
    def __init__(self):
        self.points = 0

    def update_score(self, word: str):
        """Updates the score based on the length of the word and awards bonus points for rare words."""
        base_points = len(word)  # Points based on word length
        bonus_points = self.calculate_bonus(word)  # Calculate bonus points
        self.points += base_points + bonus_points  # Update total score

    def calculate_bonus(self, word: str) -> int:
        """Calculates bonus points for rare or complex words."""
        rare_words = {"kiwi": 5, "grape": 3}  # Example of rare words with bonus points
        return rare_words.get(word, 0)  # Return bonus points if the word is rare, else 0

    def get_score(self) -> int:
        """Returns the current score."""
        return self.points