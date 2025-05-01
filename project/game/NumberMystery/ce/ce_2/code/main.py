import pygame
from game import Game

class Main:
    def main(self) -> str:
        pygame.init()
        game = Game()
        game.load_puzzles()
        game.load_hints()
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Here you would typically update the game state and render the UI
        pygame.quit()
        return "Game exited."

if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()