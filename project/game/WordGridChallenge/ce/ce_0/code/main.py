import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.start_game(0)  # Start the game at level 0

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()