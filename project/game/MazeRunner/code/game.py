import pygame
import json
from player import Player
from maze import Maze
from timer import Timer
from score import Score

class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze()
        self.timer = Timer()
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Maze Game")
        self.running = True
        self.level = 1
        self.max_levels = 3

    def start_game(self):
        self.load_maze(f'mazes_level_{self.level}.json')
        self.timer.start()
        while self.running:
            self.update()
            self.draw()
            self.handle_events()
            if self.player.stars_collected >= 5:  # Example condition to advance levels
                self.level_up()
        self.save_progress('progress.txt')

    def level_up(self):
        if self.level < self.max_levels:
            self.level += 1
            self.load_maze(f'mazes_level_{self.level}.json')
            self.player.reset()  # Reset player for new level
            self.timer.start()  # Restart timer for new level

    def update(self):
        self.player.move()
        if self.player.collect_star():
            self.score.calculate_score(self.timer.get_elapsed_time(), self.player.stars_collected, self.player.moves)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        self.timer.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def load_maze(self, file: str) -> None:
        with open(file, 'r') as f:
            maze_data = json.load(f)
            self.maze.layout = maze_data['layout']
            self.maze.obstacles = maze_data['obstacles']

    def save_progress(self, file: str) -> None:
        progress_data = {
            'player_position': self.player.position,
            'stars_collected': self.player.stars_collected,
            'level': self.level
        }
        with open(file, 'w') as f:
            json.dump(progress_data, f)