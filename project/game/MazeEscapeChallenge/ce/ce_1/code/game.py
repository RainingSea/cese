import time

class Game:
    def __init__(self, maze: Maze, player: Player):
        self.maze = maze
        self.player = player
        self.start_time = 0.0

    def start_game(self) -> None:
        self.start_time = time.time()
        self.player.start_time = self.start_time

    def restart_level(self) -> None:
        self.player.position = (1, 1)  # Reset to start position
        self.start_game()

    def end_game(self) -> None:
        self.player.reach_exit()
        FileManager.save_progress(self.player)