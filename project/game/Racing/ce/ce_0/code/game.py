import pygame
import random

class Obstacle:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.type = random.choice([True, False])  # True for slow down, False for game over
        self.position = 0  # Starting position off-screen

    def move(self):
        self.position += 5  # Move the obstacle down the screen

    def check_collision(self, vehicle):
        # Check if the obstacle's lane matches the vehicle's lane and if they collide
        return self.lane == vehicle.lane and self.position >= vehicle.position

class Game:
    def __init__(self):
        self.speed = 0
        self.distance = 0
        self.obstacles = []
        self.vehicle = Vehicle()

    def start_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.handle_input(pygame.event.get())
            self.update()
            self.draw()
            clock.tick(60)

    def update(self):
        self.distance += self.speed
        for obstacle in self.obstacles:
            obstacle.move()
            if obstacle.check_collision(self.vehicle):
                if obstacle.type:
                    self.speed -= 5  # Slow down
                else:
                    self.end_game()  # Game over

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.speed += 5
                elif event.key == pygame.K_DOWN:
                    self.speed = max(0, self.speed - 5)
                elif event.key == pygame.K_LEFT:
                    self.vehicle.change_lane(-1)
                elif event.key == pygame.K_RIGHT:
                    self.vehicle.change_lane(1)
                elif event.key == pygame.K_s:
                    self.speed = 0  # Stop the vehicle

    def draw(self):
        # Placeholder for drawing the game elements
        pass

    def end_game(self):
        # Placeholder for ending the game
        pass

class Vehicle:
    def __init__(self):
        self.lane = 1  # Start in the center lane
        self.position = 0  # Starting position

    def change_lane(self, direction):
        new_lane = self.lane + direction
        if 0 <= new_lane <= 2:
            self.lane = new_lane