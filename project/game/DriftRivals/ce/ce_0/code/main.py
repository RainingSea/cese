import pygame
from game import Game

class Main:
    def main(self) -> str:
        pygame.init()
        game = Game()
        game.start_game()
        return "Game has started."

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()