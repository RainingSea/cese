import pygame
from game import Game

def main() -> None:
    pygame.init()
    game = Game()
    
    # Initialize game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Number Puzzle Game")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and rendering would go here
        screen.fill((255, 255, 255))
        puzzle_text = game.display_puzzle()
        # Render puzzle_text to the screen here (omitted for brevity)

        pygame.display.flip()

    pygame.quit()
    
if __name__ == "__main__":
    main()