import pygame
from game import Game

class Main:
    def main(self) -> str:
        pygame.init()
        game = Game()
        game.run()
        pygame.quit()
        return "Game exited"

if __name__ == "__main__":
    main = Main()
    main.main()