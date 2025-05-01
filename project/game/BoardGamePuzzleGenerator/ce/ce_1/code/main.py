import pygame
from puzzles import Game

class Main:
    def main(self):
        pygame.init()
        game = Game()
        game.start_game("logic")  # Starting with a default category for demonstration
        pygame.quit()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()