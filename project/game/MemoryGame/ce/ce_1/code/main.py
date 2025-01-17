import pygame
from game import Game

class Main:
    def __init__(self):
        self.game = Game()

    def main(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Memory Game")
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))  # Clear screen
            # Here would be the code to render cards and handle game logic
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    app = Main()
    app.main()