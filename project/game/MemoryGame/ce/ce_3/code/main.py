import pygame
from memory_game import MemoryGame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    
    game = MemoryGame()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events like card flipping and restarting the game

        # Update game state and draw everything
        screen.fill((255, 255, 255))  # Clear screen with white
        # Draw cards and other UI elements here

        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()