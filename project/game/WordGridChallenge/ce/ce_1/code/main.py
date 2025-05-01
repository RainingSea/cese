import pygame
from game import GameEngine

def main():
    pygame.init()
    game_engine = GameEngine()
    game_engine.start_game()
    pygame.quit()

if __name__ == "__main__":
    main()