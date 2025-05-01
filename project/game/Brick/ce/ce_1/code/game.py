import pygame
import random

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = self.create_bricks()
        self.score = 0

    def create_bricks(self):
        bricks = []
        for i in range(5):  # 5 rows of bricks
            for j in range(10):  # 10 bricks per row
                bricks.append(Brick(lives=1))
        return bricks

    def start_game(self):
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Brick Breaker")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.paddle.move_left() if event.key == pygame.K_LEFT else self.paddle.move_right()

            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def update(self):
        self.ball.update_position()
        self.ball.check_collision()

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear screen
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)

class Paddle:
    def __init__(self):
        self.position = 400

    def move_left(self):
        self.position -= 10

    def move_right(self):
        self.position += 10

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position, 550, 100, 20))

class Ball:
    def __init__(self):
        self.position = [400, 300]
        self.velocity = [5, -5]

    def update_position(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def check_collision(self):
        # Check for wall collisions
        if self.position[0] <= 0 or self.position[0] >= 780:  # 800 - ball diameter
            self.velocity[0] = -self.velocity[0]
        if self.position[1] <= 0:
            self.velocity[1] = -self.velocity[1]

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position[0]), int(self.position[1])), 10)

class Brick:
    def __init__(self, lives):
        self.lives = lives
        self.position = (random.randint(0, 750), random.randint(0, 300))  # Random position for demo

    def hit(self):
        self.lives -= 1

    def draw(self, screen):
        if self.lives > 0:
            pygame.draw.rect(screen, (255, 0, 0), (*self.position, 50, 20))