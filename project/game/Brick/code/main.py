import pygame
from game import Game

class Main:
    def main(self) -> str:
        pygame.init()
        game = Game()
        game.load_game_state()  # Load game state at the start
        game.start_game()
        game.save_game_state()  # Save game state at the end
        pygame.quit()
        return "Game Over"

if __name__ == "__main__":
    main = Main()
    main.main()