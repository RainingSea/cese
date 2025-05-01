import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_progress()
    game.start_puzzle("default_image.png", "easy")
    pygame.quit()

if __name__ == "__main__":
    main()