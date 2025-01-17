import pygame
import random

class Frog:
    def __init__(self, x, y, jump_height):
        self.x = x
        self.y = y
        self.jump_height = jump_height

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def jump(self):
        self.y -= self.jump_height

class Platform:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = 800  # Reset to right side of the screen

class Game:
    def __init__(self):
        self.frog = Frog(400, 300, 50)
        self.platforms = [Platform(random.randint(800, 1200), random.randint(200, 400), 100, 20, random.randint(3, 7)) for _ in range(5)]
        self.score = 0
        self.timer = 60.0  # 60 seconds timer

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jumping Frog")
        self.clock = pygame.time.Clock()

    def update(self):
        self.timer -= 1 / 60  # Decrease timer based on frame rate
        for platform in self.platforms:
            platform.move()

    def draw(self):
        self.screen.fill((0, 0, 255))  # Fill the background with blue (water)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), (platform.x, platform.y, platform.width, platform.height))  # Draw platforms
        pygame.draw.rect(self.screen, (255, 0, 0), (self.frog.x, self.frog.y, 30, 30))  # Draw frog
        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.frog.move_left()
        if keys[pygame.K_RIGHT]:
            self.frog.move_right()
        if keys[pygame.K_SPACE]:
            self.frog.jump()

    def check_collisions(self):
        for platform in self.platforms:
            if (self.frog.x < platform.x + platform.width and
                self.frog.x + 30 > platform.x and
                self.frog.y + 30 > platform.y and
                self.frog.y < platform.y + platform.height):
                self.score += 1  # Increment score on collision

    def save_score(self):
        with open('score.txt', 'w') as score_file:
            score_file.write(str(self.score))