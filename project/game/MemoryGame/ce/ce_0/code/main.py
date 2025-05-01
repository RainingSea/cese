import pygame
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.game = Game()

    def main(self):
        self.game.run()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()