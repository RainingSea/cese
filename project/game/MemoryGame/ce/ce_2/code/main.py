import pygame
from game import Game

def main() -> None:
    pygame.init()
    num_pairs = 8  # Example number of pairs
    game = Game(num_pairs)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen with white
        # Here you would add code to draw the cards and handle user input

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()