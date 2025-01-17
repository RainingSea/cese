import pygame
from maze import Maze
from player import Player
from timer import Timer
from score import Score

class Game:
    def __init__(self):
        self.maze = Maze()
        self.player = Player()
        self.timer = Timer()
        self.score = Score()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Slide Maze Challenge")
        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        self.load_maze(0)
        self.timer.start()
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)
        self.save_scores()

    def reset_maze(self):
        self.load_maze(0)

    def load_maze(self, level: int):
        self.maze.load_from_file('mazes.txt')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move('left')
                elif event.key == pygame.K_RIGHT:
                    self.player.move('right')
                elif event.key == pygame.K_UP:
                    self.player.move('up')
                elif event.key == pygame.K_DOWN:
                    self.player.move('down')

    def render(self):
        self.screen.fill((255, 255, 255))
        self.maze.render(self.screen)
        self.player.render(self.screen)
        pygame.display.flip()

    def save_scores(self):
        with open('scores.txt', 'a') as f:
            f.write(f"Score: {self.score.get_score()}\n")