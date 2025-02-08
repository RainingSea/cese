import pygame
import sys
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Letter Connection Game")

    game = Game()
    game.start_game("easy")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Game loop logic (not implemented)
        screen.fill((255, 255, 255))  # Clear screen with white
        pygame.display.flip()

if __name__ == "__main__":
    main()