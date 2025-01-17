import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self):
        self.paddle = Paddle(300, 100)
        self.ball = Ball(400, 300)
        self.bricks = [Brick(x * 55, 50, 1) for x in range(10)]

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT]:
                self.paddle.move_right()

            self.ball.move()
            self.check_collisions()

            screen.fill((0, 0, 0))
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw(self, surface):
        self.paddle.draw(surface)
        self.ball.draw(surface)
        for brick in self.bricks:
            brick.draw(surface)

    def check_collisions(self):
        # Check for ball collisions with paddle
        if (self.ball.y + 10 >= 380 and self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width):
            self.ball.dy *= -1

        # Check for ball collisions with bricks
        for brick in self.bricks:
            if (brick.lives > 0 and
                brick.x <= self.ball.x <= brick.x + 50 and
                brick.y <= self.ball.y <= brick.y + 20):
                brick.hit()
                self.ball.dy *= -1