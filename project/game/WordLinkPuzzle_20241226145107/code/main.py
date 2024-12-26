import pygame
import sys
from game import Game

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 4
CELL_SIZE = 100
FONT_SIZE = 36
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Word Formation Game")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.game = Game()
        self.running = True

    def draw_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                letter = self.game.grid.letters[row][col]
                pygame.draw.rect(self.screen, GRID_COLOR, 
                                 (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                text_surface = self.font.render(letter, True, TEXT_COLOR)
                self.screen.blit(text_surface, 
                                 (col * CELL_SIZE + (CELL_SIZE - text_surface.get_width()) // 2,
                                  row * CELL_SIZE + (CELL_SIZE - text_surface.get_height()) // 2))

    def draw_score(self):
        score_text = f"Score: {self.game.score.get_score()}"
        text_surface = self.font.render(score_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (10, SCREEN_HEIGHT - 40))

    def draw_words(self):
        words_text = "Words: " + ", ".join(self.game.grid.selected_letters)
        text_surface = self.font.render(words_text, True, TEXT_COLOR)
        self.screen.blit(text_surface, (10, SCREEN_HEIGHT - 80))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_grid()
            self.draw_score()
            self.draw_words()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ui = GameUI()
    ui.run()