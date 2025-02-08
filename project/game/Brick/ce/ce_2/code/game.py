import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.paddle = Paddle(width // 2 - 30, 60)
        self.ball = Ball(width // 2, height // 2)
        self.bricks = []
        self.load_bricks()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()

        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()

    def update(self):
        self.ball.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.paddle.draw(screen)
        self.ball.draw(screen)
        for brick in self.bricks:
            brick.draw(screen)

    def load_bricks(self):
        try:
            with open('bricks.txt', 'r') as file:
                for line in file:
                    x, y, lives = map(int, line.strip().split('|'))
                    self.bricks.append(Brick(x, y, lives))
        except FileNotFoundError:
            # If the file doesn't exist, create default bricks
            for i in range(5):
                self.bricks.append(Brick(10 + i * 70, 50, 1))

    def save_bricks(self):
        with open('bricks.txt', 'w') as file:
            for brick in self.bricks:
                file.write(f"{brick.x}|{brick.y}|{brick.lives}\n")