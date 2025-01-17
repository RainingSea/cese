import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    game.load_shapes()
    game.load_patterns()

    # Setup game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Geometric Shapes Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white background
        game.draw()  # Draw shapes on the screen
        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()