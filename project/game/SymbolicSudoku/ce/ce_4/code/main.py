import pygame
from pygame.locals import *
from game import Game, Difficulty

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Symbolic Sudoku Challenge")
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                # Handle mouse input for symbol placement
                pass

        screen.fill((255, 255, 255))
        # Draw the Sudoku grid and other UI elements
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()