import time
from maze import Maze
from player import Player

class Game:
    def __init__(self, maze: Maze, player: Player):
        self.maze = maze
        self.player = player
        self.start_time = 0.0

    def run(self) -> None:
        self.start_time = time.time()
        while not self.check_exit():
            self.maze.display()
            move = input("Enter move (up, down, left, right): ")
            self.player.move(move)

        self.player.set_time(time.time() - self.start_time)
        self.save_stats()

    def check_exit(self) -> bool:
        return self.player.position == (self.maze.height - 2, self.maze.width - 1)

    def save_stats(self) -> None:
        with open('player_stats.txt', 'a') as f:
            f.write(f"{self.player.time_taken}\n")