import pygame
from player import Player
from maze import Maze
from star import Star
from timer import Timer
from score import Score
from progress import Progress

class Game:
    def __init__(self):
        self.player = Player()
        self.maze = Maze()
        self.timer = Timer()
        self.score = Score()
        self.progress = Progress()
        self.stars = []
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_level = 1

    def start_game(self):
        self.load_level(self.current_level)
        self.timer.start()
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)

    def load_level(self, level: int):
        self.maze.generate_maze(level)
        self.load_stars(level)
        self.progress.load_progress(self.player.name)

    def load_stars(self, level: int):
        star_positions = [(1, 1), (2, 2), (3, 3)]  # Example star positions
        self.stars = [Star(pos) for pos in star_positions]

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move("left", self.maze)
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right", self.maze)
                elif event.key == pygame.K_UP:
                    self.player.move("up", self.maze)
                elif event.key == pygame.K_DOWN:
                    self.player.move("down", self.maze)
                self.check_star_collection()

    def check_star_collection(self):
        for star in self.stars:
            if not star.is_collected() and self.player.position == star.position:
                star.collected = True
                self.player.collect_star()
                self.score.update_score(1, self.timer.get_elapsed_time(), 0)  # Update score
                self.progress.update_progress(self.player.name, self.score.points)

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        self.maze.render(self.screen)
        self.player.render(self.screen)
        for star in self.stars:
            if not star.is_collected():
                star.render(self.screen)
        self.score.render(self.screen)
        pygame.display.flip()