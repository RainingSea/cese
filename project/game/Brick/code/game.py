import pygame
import json
import os

class Paddle:
    def __init__(self, position_x: int, width: int):
        self.position_x = position_x
        self.width = width

    def move(self, direction: str):
        if direction == 'left':
            self.position_x = max(0, self.position_x - 10)  # Prevent moving out of bounds
        elif direction == 'right':
            self.position_x = min(800 - self.width, self.position_x + 10)  # Prevent moving out of bounds

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position_x, 550, self.width, 10))


class Ball:
    def __init__(self, position_x: int, position_y: int):
        self.reset()

    def reset(self):
        self.position_x = 400
        self.position_y = 300
        self.velocity_x = 5
        self.velocity_y = -5

    def move(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

    def bounce(self, direction: str):
        if direction == 'horizontal':
            self.velocity_y = -self.velocity_y
        elif direction == 'vertical':
            self.velocity_x = -self.velocity_x

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.position_x, self.position_y), 10)


class Brick:
    def __init__(self, lives: int):
        self.lives = lives

    def hit(self):
        self.lives -= 1

    def is_destroyed(self):
        return self.lives <= 0

    def draw(self, screen, position_x, position_y):
        if not self.is_destroyed():
            pygame.draw.rect(screen, (255, 0, 0), (position_x, position_y, 60, 20))


class Game:
    def __init__(self):
        self.paddle = Paddle(400, 100)
        self.ball = Ball(400, 300)
        self.bricks = self.load_bricks()
        self.score = 0
        self.lives = 3

    def load_bricks(self):
        if os.path.exists('bricks.txt'):
            with open('bricks.txt', 'r') as f:
                return [Brick(int(line.strip())) for line in f.readlines() if line.strip().isdigit()]
        else:
            raise FileNotFoundError("The required 'bricks.txt' file is missing.")

    def start_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.load_game_state()

    def update(self):
        self.ball.move()
        if self.ball.position_x <= 0 or self.ball.position_x >= 800:
            self.ball.bounce('vertical')
        if self.ball.position_y <= 0:
            self.ball.bounce('horizontal')
        if self.ball.position_y >= 600:
            self.lives -= 1
            self.ball.reset()

        # Paddle collision detection
        if (self.ball.position_y >= 540 and 
            self.paddle.position_x <= self.ball.position_x <= self.paddle.position_x + self.paddle.width):
            self.ball.bounce('horizontal')

        for index, brick in enumerate(self.bricks):
            if not brick.is_destroyed() and self.ball.position_y <= 20 and \
               (self.ball.position_x >= index * 60 and self.ball.position_x <= (index + 1) * 60):
                brick.hit()
                self.ball.bounce('horizontal')
                if brick.is_destroyed():
                    self.score += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for index, brick in enumerate(self.bricks):
            brick.draw(self.screen, index * 60, 20)
        pygame.display.flip()

    def save_game_state(self):
        game_state = {
            'score': self.score,
            'lives': self.lives,
            'bricks': [brick.lives for brick in self.bricks]
        }
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self):
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
                self.score = game_state['score']
                self.lives = game_state['lives']
                for i in range(len(self.bricks)):
                    self.bricks[i].lives = game_state['bricks'][i]
        except (FileNotFoundError, json.JSONDecodeError):
            pass