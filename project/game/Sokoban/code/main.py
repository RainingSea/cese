import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_state('game_state.txt')
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()