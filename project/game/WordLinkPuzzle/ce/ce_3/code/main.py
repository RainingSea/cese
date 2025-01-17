import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Letter Connection Game")

    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the display
        pygame.display.flip()

    game.save_progress()
    pygame.quit()

if __name__ == "__main__":
    main()