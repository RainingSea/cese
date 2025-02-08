import pygame
import random

class Obstacle:
    def __init__(self, lane: int, is_hazard: bool):
        self.lane = lane
        self.is_hazard = is_hazard
        self.y_position = 0  # Start at the top of the screen

    def move(self):
        self.y_position += 5  # Move down the screen

class Vehicle:
    def __init__(self):
        self.lane = 1  # Start in the middle lane
        self.speed = 0.0

    def move_up(self):
        if self.lane > 0:
            self.lane -= 1

    def move_down(self):
        if self.lane < 2:
            self.lane += 1

    def shift_left(self):
        if self.lane > 0:
            self.lane -= 1

    def shift_right(self):
        if self.lane < 2:
            self.lane += 1

    def stop(self):
        self.speed = 0.0

class Game:
    def __init__(self):
        self.vehicle = Vehicle()
        self.obstacles = []
        self.speed = 0.0
        self.distance = 0.0
        self.load_obstacles()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            clock.tick(60)

        pygame.quit()

    def update(self):
        for obstacle in self.obstacles:
            obstacle.move()
        self.distance += self.speed / 60

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Clear screen
        # Draw vehicle
        pygame.draw.rect(screen, (0, 0, 255), (self.vehicle.lane * 100 + 50, 500, 50, 100))
        # Draw obstacles
        for obstacle in self.obstacles:
            color = (255, 0, 0) if obstacle.is_hazard else (0, 255, 0)
            pygame.draw.rect(screen, color, (obstacle.lane * 100 + 50, obstacle.y_position, 50, 50))
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vehicle.move_up()
                elif event.key == pygame.K_DOWN:
                    self.vehicle.move_down()
                elif event.key == pygame.K_LEFT:
                    self.vehicle.shift_left()
                elif event.key == pygame.K_RIGHT:
                    self.vehicle.shift_right()

    def load_obstacles(self):
        with open('obstacles.txt', 'r') as file:
            for line in file:
                lane, is_hazard = line.strip().split('|')
                self.obstacles.append(Obstacle(int(lane), is_hazard == 'True'))

    def save_game_state(self):
        with open('game_state.txt', 'w') as file:
            file.write(f"Speed: {self.speed}\n")
            file.write(f"Distance: {self.distance}\n")