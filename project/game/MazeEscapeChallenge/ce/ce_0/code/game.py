from timer import Timer
from maze import Maze
from player import Player

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()

    def start_game(self):
        self.maze.generate_maze(10)  # Example size
        self.timer.start()
        # Game loop would go here

    def restart_level(self):
        self.player.position_x = 0
        self.player.position_y = 0
        self.start_game()

    def exit_game(self):
        # Exit logic would go here
        pass