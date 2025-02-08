import pygame
import sys
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Number Connect Game")

    game = Game()
    game.start_game(4)  # Start with a grid of size 4

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        game.grid.draw_grid(screen)

        pygame.display.flip()
        game.update_timer()
        clock.tick(1)  # Update the timer every second

if __name__ == "__main__":
    main()