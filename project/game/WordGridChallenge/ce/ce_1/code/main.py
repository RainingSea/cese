import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.start_game()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Game rendering and logic would go here

    pygame.quit()

if __name__ == "__main__":
    main()