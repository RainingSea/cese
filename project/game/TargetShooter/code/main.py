import pygame
from game import Game

class Main:
    def main(self) -> str:
        pygame.init()
        pygame.font.init()  # Ensure font is initialized
        game = Game()
        game.start_game()
        pygame.quit()
        return "Game Over"

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()