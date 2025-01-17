import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.start_game()

    # Game loop placeholder
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    return "Game exited."

if __name__ == "__main__":
    main()