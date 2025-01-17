import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.load_progress()
    game.start_game()  # Placeholder for starting the game loop

if __name__ == "__main__":
    main()