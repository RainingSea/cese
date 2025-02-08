import pygame
from game import Game

def main() -> str:
    pygame.init()
    game = Game()
    game.start_game("Logic Puzzles")
    pygame.quit()
    return "Game ended"

if __name__ == "__main__":
    main()