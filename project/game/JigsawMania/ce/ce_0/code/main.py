import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game("default_image.png", "easy")  # Starting with a default image and difficulty
    pygame.quit()

if __name__ == "__main__":
    main()