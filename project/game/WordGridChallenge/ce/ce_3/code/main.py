import pygame
from pygame.locals import *
from word_list import WordList
from score_storage import ScoreStorage
from game import Game

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Word Grid Challenge")

    # Load word list and score storage
    word_list = WordList('word_list.txt')
    score_storage = ScoreStorage('scores.json')

    # Create game instance
    game = Game()
    game.start_game()

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fill the screen with white
        # Draw game elements here (grid, score, timer)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()