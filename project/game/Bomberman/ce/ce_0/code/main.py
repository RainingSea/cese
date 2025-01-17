import pygame
from game import Game

def main():
    grid_size = 13
    game = Game(grid_size)
    game.run()

if __name__ == "__main__":
    main()