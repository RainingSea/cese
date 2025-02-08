import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Word Grid Challenge")

    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        game.display_grid()  # Example display call
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()