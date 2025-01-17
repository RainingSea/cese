import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Number Connection Game")
    
    game = Game()
    game.start_game(level=1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update game state
        game.update_timer()

        # Render game screen
        screen.fill((255, 255, 255))
        # Code to draw grid and timer would go here
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()