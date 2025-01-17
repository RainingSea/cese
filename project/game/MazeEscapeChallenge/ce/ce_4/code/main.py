import pygame
from maze import Maze
from player import Player
from game import Game

def main():
    pygame.init()
    maze = Maze(21, 21)
    player = Player((1, 0))
    game = Game(maze, player)
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()