import pygame
import random

class Paddle:
    def __init__(self):
        self.position = 400

    def move_left(self):
        self.position -= 10
        if self.position < 0:
            self.position = 0

    def move_right(self):
        self.position += 10
        if self.position > 700:
            self.position = 700

class Ball:
    def __init__(self):
        self.position = [400, 300]
        self.velocity = [5, -5]

    def update_position(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def bounce(self):
        self.velocity[1] = -self.velocity[1]

class Brick:
    def __init__(self):
        self.lives = 1

    def hit(self):
        self.lives -= 1
        if self.lives <= 0:
            return True
        return False

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick() for _ in range(10)]
        self.score = 0

    def start_game(self):
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.paddle.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.paddle.move_right()

            self.update()
            self.draw(screen)
            self.handle_collisions()
            pygame.display.flip()
            clock.tick(60)

    def update(self):
        self.ball.update_position()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (self.paddle.position, 580, 100, 20))
        pygame.draw.circle(screen, (255, 0, 0), (self.ball.position[0], self.ball.position[1]), 10)
        for i, brick in enumerate(self.bricks):
            if brick.lives > 0:
                pygame.draw.rect(screen, (0, 255, 0), (i * 60, 50, 60, 20))

    def handle_collisions(self):
        if (self.ball.position[0] <= 0 or self.ball.position[0] >= 790):
            self.ball.bounce()
        if self.ball.position[1] <= 0:
            self.ball.bounce()
        if (self.ball.position[1] >= 570 and 
            self.paddle.position <= self.ball.position[0] <= self.paddle.position + 100):
            self.ball.bounce()

        for brick in self.bricks:
            if brick.lives > 0 and self.ball.position[1] <= 70:
                brick.hit()
                self.score += 10
                self.ball.bounce()