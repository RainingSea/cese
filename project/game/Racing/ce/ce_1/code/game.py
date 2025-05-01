import pygame
import random
from car import Car
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.car = Car()
        self.obstacles = []
        self.score = 0
        self.is_running = True
        self.window_width = 800
        self.window_height = 600
        self.lane_height = self.window_height // 3
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Racing Game")

    def start(self):
        clock = pygame.time.Clock()
        while self.is_running:
            self.handle_input()
            self.update()
            self.render()
            clock.tick(60)

    def update(self):
        if random.randint(1, 20) == 1:  # Randomly generate obstacles
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(lane))
        for obstacle in self.obstacles:
            obstacle.move()
        self.check_collision()

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (255, 0, 0), (obstacle.lane * (self.window_width // 3), obstacle.y, 50, 50))
        pygame.draw.rect(self.screen, (0, 0, 255), (self.car.lane * (self.window_width // 3) + 25, self.window_height - 100, 50, 50))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.car.move_up()
                elif event.key == pygame.K_DOWN:
                    self.car.move_down()
                elif event.key == pygame.K_s:
                    self.car.stop()

    def check_collision(self):
        for obstacle in self.obstacles:
            if obstacle.lane == self.car.lane and obstacle.y + 50 > self.window_height - 100:
                self.is_running = False  # End game on collision