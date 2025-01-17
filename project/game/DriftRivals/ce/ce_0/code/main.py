import pygame
from game import Game

def main():
    pygame.init()
    game_instance = Game()
    game_instance.run()
    pygame.quit()

if __name__ == "__main__":
    main()