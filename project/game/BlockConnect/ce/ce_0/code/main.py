import pygame
from game import Game

def main():
    pygame.init()
    game = Game()
    game.load_game_state()
    
    while True:
        game.handle_events()
        game.update()
        game.render()

if __name__ == "__main__":
    main()