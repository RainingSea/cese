import pygame
from pygame.locals import *
from random import randint

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Paddle:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)

    def move_left(self) -> None:
        if self.position[0] > 0:
            self.position = (self.position[0] - 10, self.position[1])

    def move_right(self) -> None:
        if self.position[0] < SCREEN_WIDTH - PADDLE_WIDTH:
            self.position = (self.position[0] + 10, self.position[1])

class Ball:
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = (5, -5)

    def update_position(self) -> None:
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

    def bounce(self) -> None:
        self.velocity = (self.velocity[0], -self.velocity[1])

    def check_collision(self, paddle: Paddle, bricks: list) -> None:
        # Check collision with paddle
        if (self.position[1] + BALL_RADIUS >= paddle.position[1] and
            paddle.position[0] <= self.position[0] <= paddle.position[0] + PADDLE_WIDTH):
            self.bounce()

        # Check collision with walls
        if self.position[0] - BALL_RADIUS <= 0 or self.position[0] + BALL_RADIUS >= SCREEN_WIDTH:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.position[1] - BALL_RADIUS <= 0:
            self.velocity = (self.velocity[0], -self.velocity[1])

        # Check collision with bricks
        for brick in bricks:
            if (brick.lives > 0 and
                brick.position[0] <= self.position[0] <= brick.position[0] + BRICK_WIDTH and
                brick.position[1] <= self.position[1] <= brick.position[1] + BRICK_HEIGHT):
                if brick.hit():  # Check if brick is destroyed
                    self.bounce()

class Brick:
    def __init__(self, position):
        self.position = position
        self.lives = 1

    def hit(self) -> bool:
        self.lives -= 1
        return self.lives <= 0  # Return True if brick is destroyed

class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick((x * BRICK_WIDTH, y * BRICK_HEIGHT)) for x in range(10) for y in range(5)]
        self.score = 0  # Initialize score
        self.lives = 3  # Initialize lives

    def start_game(self) -> None:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                self.paddle.move_left()
            if keys[K_RIGHT]:
                self.paddle.move_right()

            self.ball.update_position()
            self.ball.check_collision(self.paddle, self.bricks)

            # Check for end game condition
            if self.ball.position[1] > SCREEN_HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    print("Game Over")
                    running = False
                else:
                    self.reset_ball()

            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (0, 0, 255), (*self.paddle.position, PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.circle(screen, (0, 255, 0), (int(self.ball.position[0]), int(self.ball.position[1])), BALL_RADIUS)
            for brick in self.bricks:
                if brick.lives > 0:
                    pygame.draw.rect(screen, (255, 0, 0), (*brick.position, BRICK_WIDTH, BRICK_HEIGHT))

            pygame.display.flip()
            clock.tick(60)

    def reset_ball(self) -> None:
        self.ball.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.ball.velocity = (5, -5)

    def save_game_state(self) -> None:
        with open('game_data.txt', 'w') as f:
            f.write(f'lives: {self.lives}\n')  # Save lives
            f.write(f'score: {self.score}\n')  # Save score

    def load_game_state(self) -> None:
        try:
            with open('game_data.txt', 'r') as f:
                data = f.readlines()
                for line in data:
                    if line.startswith('lives:'):
                        self.lives = int(line.split(':')[1].strip())
                        print(f"Lives loaded: {self.lives}")
                    elif line.startswith('score:'):
                        self.score = int(line.split(':')[1].strip())
                        print(f"Score loaded: {self.score}")
        except FileNotFoundError:
            print("No saved game state found.")