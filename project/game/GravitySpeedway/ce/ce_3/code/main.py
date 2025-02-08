import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.start_game()
    return "Game started"

if __name__ == "__main__":
    main()