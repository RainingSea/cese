import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Number Connect Game")
    clock = pygame.time.Clock()
    
    game = Game()
    game.start_game(level=1)  # Start the game with level 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Convert pixel position to grid coordinates
                grid_x = x // 100  # Assuming each tile is 100 pixels wide
                grid_y = y // 100  # Assuming each tile is 100 pixels tall
                game.click_tile(grid_x, grid_y)

        # Update timer
        game.timer.update_timer()

        # Drawing logic goes here
        screen.fill((255, 255, 255))  # Clear screen with white
        # Draw grid and other UI elements

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()