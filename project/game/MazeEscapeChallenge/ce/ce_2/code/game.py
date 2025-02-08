import pygame
from maze import Maze
from timer import Timer
from player import Player

class Game:
    def __init__(self):
        self.maze = Maze()
        self.timer = Timer()
        self.player = Player()

    def start_game(self) -> None:
        self.maze.generate(size=10)
        self.timer.start()

    def generate_maze(self, size: int, difficulty: str) -> None:
        self.maze.generate(size)

    def handle_input(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player.move('up')
            elif event.key == pygame.K_DOWN:
                self.player.move('down')
            elif event.key == pygame.K_LEFT:
                self.player.move('left')
            elif event.key == pygame.K_RIGHT:
                self.player.move('right')

    def check_exit(self) -> bool:
        return self.maze.is_exit_reached(self.player.get_position())

    def restart_game(self) -> None:
        self.start_game()