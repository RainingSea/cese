import pygame
import os

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLUMNS = 10

# File paths
SCORES_FILE = 'scores.txt'
GAME_STATE_FILE = 'game_state.txt'

class Main:
    @staticmethod
    def main():
        pygame.init()
        game = Game()
        game.start_game()
        pygame.quit()

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = self.create_bricks()
        self.running = True

    def create_bricks(self):
        bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLUMNS):
                bricks.append(Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, 1))
        return bricks

    def start_game(self):
        self.ball.launch()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()

    def update(self):
        self.ball.bounce(self.paddle, self.bricks)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.paddle.draw(self.window)
        self.ball.draw(self.window)
        for brick in self.bricks:
            brick.draw(self.window)
        pygame.display.flip()

class Paddle:
    def __init__(self):
        self.position = (WINDOW_WIDTH // 2 - PADDLE_WIDTH // 2, WINDOW_HEIGHT - PADDLE_HEIGHT - 10)

    def move_left(self):
        if self.position[0] > 0:
            self.position = (self.position[0] - 10, self.position[1])

    def move_right(self):
        if self.position[0] < WINDOW_WIDTH - PADDLE_WIDTH:
            self.position = (self.position[0] + 10, self.position[1])

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), (self.position[0], self.position[1], PADDLE_WIDTH, PADDLE_HEIGHT))

class Ball:
    def __init__(self):
        self.position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        self.velocity = [5, -5]

    def launch(self):
        self.position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]

    def bounce(self, paddle, bricks):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Bounce off walls
        if self.position[0] <= 0 or self.position[0] >= WINDOW_WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] <= 0:
            self.velocity[1] = -self.velocity[1]

        # Bounce off paddle
        if (paddle.position[0] < self.position[0] < paddle.position[0] + PADDLE_WIDTH and
                paddle.position[1] < self.position[1] + BALL_RADIUS < paddle.position[1] + PADDLE_HEIGHT):
            self.velocity[1] = -self.velocity[1]

        # Check for brick collisions
        for brick in bricks:
            if brick.is_hit(self.position):
                brick.hit()
                self.velocity[1] = -self.velocity[1]
                break

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (int(self.position[0]), int(self.position[1])), BALL_RADIUS)

class Brick:
    def __init__(self, x, y, lives):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.lives = lives

    def hit(self):
        self.lives -= 1

    def is_hit(self, ball_position):
        return self.rect.collidepoint(ball_position[0], ball_position[1])

    def draw(self, window):
        if self.lives > 0:
            pygame.draw.rect(window, (255, 0, 0), self.rect)

if __name__ == "__main__":
    Main.main()