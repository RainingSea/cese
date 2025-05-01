import pygame
import random

class Frog:
    def __init__(self):
        self.position_x = 300
        self.position_y = 400

    def move_left(self):
        self.position_x -= 10

    def move_right(self):
        self.position_x += 10

    def jump(self):
        self.position_y -= 50  # Jump height

class Platform:
    def __init__(self, position_x, position_y, movement_direction):
        self.position_x = position_x
        self.position_y = position_y
        self.movement_direction = movement_direction

    def move(self):
        self.position_x += self.movement_direction
        if self.position_x < 0 or self.position_x > 800:  # Assuming screen width is 800
            self.movement_direction *= -1  # Change direction if hitting the screen edge

class Game:
    def __init__(self):
        self.frog = Frog()
        self.platforms = [Platform(random.randint(0, 750), random.randint(100, 500), random.choice([-1, 1])) for _ in range(5)]
        self.score = 0
        self.timer = 60.0  # 60 seconds timer

    def start_game(self):
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.update()
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.frog.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.frog.move_right()
                    if event.key == pygame.K_SPACE:
                        self.frog.jump()

            clock.tick(60)  # Limit to 60 frames per second

    def update(self):
        for platform in self.platforms:
            platform.move()
        self.timer -= 1/60  # Decrease timer based on frame rate

    def render(self, screen):
        screen.fill((0, 0, 255))  # Fill the screen with blue (river)
        for platform in self.platforms:
            pygame.draw.rect(screen, (255, 255, 255), (platform.position_x, platform.position_y, 100, 20))  # Draw platforms
        pygame.draw.rect(screen, (0, 255, 0), (self.frog.position_x, self.frog.position_y, 30, 30))  # Draw frog
        pygame.display.flip()

    def restart(self):
        self.frog = Frog()
        self.platforms = [Platform(random.randint(0, 750), random.randint(100, 500), random.choice([-1, 1])) for _ in range(5)]
        self.score = 0
        self.timer = 60.0