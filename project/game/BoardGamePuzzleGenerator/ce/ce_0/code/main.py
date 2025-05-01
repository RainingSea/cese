import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_game("logic")  # Starting with a default category for demo
    pygame.quit()

if __name__ == "__main__":
    main()