import pygame
from maze import Maze
from player import Player
from game import Game

def main():
    pygame.init()
    maze = Maze(21, 21)
    player = Player((1, 1))
    game = Game(maze, player)

    game.start_game()
    maze.display_maze()

    # Game loop placeholder
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()