import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Color Swap Challenge")
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white
        # Placeholder for drawing game grid and blocks
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()