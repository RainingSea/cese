import pygame
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Puzzle Game")
    
    game = Game()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Placeholder for game logic and rendering
        screen.fill((255, 255, 255))  # Clear screen with white
        game.start_game('Logic')  # Example starting a game with Logic puzzles

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()