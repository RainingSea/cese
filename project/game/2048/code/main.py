import pygame
from game import Game

def main() -> None:
    """Initialize the game and start the game loop."""
    pygame.init()
    pygame.font.init()  # Ensure font module is initialized
    game = Game()
    game.start_game()
    pygame.quit()

if __name__ == "__main__":
    main()