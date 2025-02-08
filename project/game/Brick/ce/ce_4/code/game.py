import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self):
        self.paddle = Paddle(300, 100)
        self.ball = Ball(400, 300)
        self.bricks = []
        self.is_running = True
        self.load_bricks()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        while self.is_running:
            self.handle_input()
            self.update()
            self.draw(screen)
            clock.tick(60)

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move("left")
        if keys[pygame.K_RIGHT]:
            self.paddle.move("right")

    def update(self):
        self.ball.move()
        # Check for ball collision with paddle and bricks (not implemented)

    def draw(self, surface):
        surface.fill((0, 0, 0))  # Clear screen
        self.paddle.draw(surface)
        self.ball.draw(surface)
        for brick in self.bricks:
            brick.draw(surface)
        pygame.display.flip()

    def load_bricks(self):
        with open('bricks.txt', 'r') as file:
            for line in file:
                life = int(line.strip())
                self.bricks.append(Brick(life))

    def save_bricks(self):
        with open('bricks.txt', 'w') as file:
            for brick in self.bricks:
                file.write(f"{brick.life}\n")