import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.start_race()
    while True:
        game.handle_input()
        game.update()
        game.render()

if __name__ == "__main__":
    main()