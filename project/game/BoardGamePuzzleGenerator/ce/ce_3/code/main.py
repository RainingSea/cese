import pygame
import sys
from game import Game

class Main:
    def __init__(self):
        self.game = Game()

    def main(self) -> str:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Puzzle Game")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Main menu and game logic would go here
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    main_app = Main()
    main_app.main()