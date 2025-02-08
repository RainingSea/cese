import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    
    # Example of starting a game
    game.start_game('path/to/image.png', 'easy')

    # Game loop would go here

if __name__ == "__main__":
    main()