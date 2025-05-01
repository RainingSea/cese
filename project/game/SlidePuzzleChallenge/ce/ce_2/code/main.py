import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game("easy")  # Starting with easy difficulty
    pygame.quit()

if __name__ == "__main__":
    main()