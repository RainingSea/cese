import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game loop logic here
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()