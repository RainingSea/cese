import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game("puzzle_image.png", "easy")
    pygame.quit()

if __name__ == "__main__":
    main()