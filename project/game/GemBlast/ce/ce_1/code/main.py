import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gem Blast")
    
    game = Game()
    game.start_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear screen with white
        # Here you would draw the game grid, score, etc.
        
        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()