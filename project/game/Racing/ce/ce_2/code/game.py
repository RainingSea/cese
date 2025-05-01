import pygame
import random

class Vehicle:
    def __init__(self):
        self.speed = 0
        self.lane = 1  # Center lane

    def move_up(self):
        if self.lane > 0:
            self.lane -= 1

    def move_down(self):
        if self.lane < 2:
            self.lane += 1

    def stop(self):
        self.speed = 0


class Obstacle:
    def __init__(self, lane):
        self.type = random.randint(0, 2)  # Different types of obstacles
        self.position = 600  # Starting position off-screen

    def move(self):
        self.position -= 5  # Move obstacle backward

    def check_collision(self, vehicle: Vehicle) -> bool:
        # Simple collision detection
        return self.position < 100 and self.position > 0 and vehicle.lane == self.type


class Game:
    def __init__(self):
        self.vehicle = Vehicle()
        self.obstacles = []
        self.score = 0
        self.running = True
        self.screen = pygame.display.set_mode((400, 600))

    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            self.update()
            self.render()
            clock.tick(60)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vehicle.move_up()
                elif event.key == pygame.K_DOWN:
                    self.vehicle.move_down()
                elif event.key == pygame.K_s:
                    self.vehicle.stop()

        # Generate obstacles
        if random.randint(1, 20) == 1:
            lane = random.randint(0, 2)
            self.obstacles.append(Obstacle(lane))

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.check_collision(self.vehicle):
                self.running = False  # End game on collision

        # Remove off-screen obstacles
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.position > 0]

    def render(self):
        self.screen.fill((255, 255, 255))  # Clear screen
        # Draw lanes
        for i in range(3):
            pygame.draw.rect(self.screen, (200, 200, 200), (0, i * 200, 400, 200), 2)
        
        # Draw vehicle
        pygame.draw.rect(self.screen, (0, 255, 0), (150, self.vehicle.lane * 200 + 50, 100, 100))

        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (255, 0, 0), (150, obstacle.position, 100, 100))

        pygame.display.flip()