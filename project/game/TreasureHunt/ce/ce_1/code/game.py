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
        pygame.display.set_caption("Maze Treasure Hunt")
        self.clock = pygame.time.Clock()
        self.running = True

    def start_game(self):
        self.maze.generate_maze()
        self.timer.start()
        while self.running:
            self.update()
            self.render()
            self.clock.tick(60)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("up")
                elif event.key == pygame.K_DOWN:
                    self.player.move("down")
                elif event.key == pygame.K_LEFT:
                    self.player.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right")
        self.timer.update()
        if self.timer.is_time_up():
            self.running = False

    def render(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.player.draw(self.screen)
        # Display timer and score
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f'Time: {self.timer.elapsed_time}', True, (255, 255, 255))
        score_text = font.render(f'Score: {self.score.current_score}', True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 10))
        self.screen.blit(score_text, (10, 50))
        pygame.display.flip()

    def check_collision(self):
        # Logic to check for collision with maze walls or treasure
        pass

    def load_new_maze(self):
        # Logic to load a new maze
        pass