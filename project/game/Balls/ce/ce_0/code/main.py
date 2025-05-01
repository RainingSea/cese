import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.initialize()

    while True:
        game.handle_input()
        game.update()
        game.save_data()
        pygame.display.flip()

if __name__ == "__main__":
    main()