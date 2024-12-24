import pygame

class Score:
    def __init__(self):
        self.points = 0

    def calculate_score(self, word: str) -> int:
        length = len(word)
        base_score = 0
        
        if length <= 3:
            base_score = 1
        elif length <= 5:
            base_score = 2
        elif length <= 7:
            base_score = 3
        else:
            base_score = 5  # Bonus for longer words

        if length > 7:
            base_score += 2  # Additional bonus points for complex words

        return base_score

    def add_points(self, points: int):
        self.points += points

    def get_score(self) -> int:
        return self.points

    def display_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.points}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  # Display score at the top left corner