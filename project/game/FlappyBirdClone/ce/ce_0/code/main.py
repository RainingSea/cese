import pygame
from game import Game

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((600, 800))
    pygame.display.set_caption("Flappy Bird Clone")
    
    game = Game()
    game.start_game()
    
    pygame.quit()

if __name__ == "__main__":
    main()