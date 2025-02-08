import pygame
from high_scores import HighScores

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.high_scores = HighScores()
        self.high_scores.load_scores()

    def show_main_menu(self) -> None:
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 74)
        text = font.render('Color Link Puzzle', True, (0, 0, 0))
        self.screen.blit(text, (100, 100))

        start_text = font.render('Start Game', True, (0, 128, 0))
        self.screen.blit(start_text, (150, 250))

        high_scores_text = font.render('High Scores', True, (0, 0, 128))
        self.screen.blit(high_scores_text, (150, 350))

        pygame.display.flip()

    def view_high_scores(self) -> None:
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        y_offset = 50
        for name, score in self.high_scores.scores:
            score_text = font.render(f"{name}: {score}", True, (0, 0, 0))
            self.screen.blit(score_text, (50, y_offset))
            y_offset += 30

        pygame.display.flip()