import pygame
import sys
from game import Game

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 8
GEM_SIZE = 70

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gem Blast")

# Colors
COLORS = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'purple': (128, 0, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}

def draw_grid(game):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            gem = game.grid.get_gem((row, col))
            if gem:
                pygame.draw.rect(screen, COLORS[gem.color], (col * GEM_SIZE, row * GEM_SIZE, GEM_SIZE, GEM_SIZE))
            else:
                pygame.draw.rect(screen, COLORS['black'], (col * GEM_SIZE, row * GEM_SIZE, GEM_SIZE, GEM_SIZE))

def main():
    game = Game()
    game.start_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle user input for gem swapping here

        screen.fill(COLORS['white'])
        draw_grid(game)
        pygame.display.flip()

if __name__ == "__main__":
    main()