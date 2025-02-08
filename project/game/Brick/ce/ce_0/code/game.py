import pygame

class Paddle:
    def __init__(self):
        self.position_x = 300  # Initial position

    def move_left(self):
        self.position_x -= 10  # Move left by 10 pixels

    def move_right(self):
        self.position_x += 10  # Move right by 10 pixels

    def get_position(self):
        return self.position_x


class Ball:
    def __init__(self):
        self.position_x = 400  # Initial position
        self.position_y = 300  # Initial position
        self.velocity_x = 5     # Initial horizontal velocity
        self.velocity_y = -5    # Initial vertical velocity

    def update(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y

    def reset(self):
        self.position_x = 400
        self.position_y = 300
        self.velocity_x = 5
        self.velocity_y = -5


class Brick:
    def __init__(self, position_x, position_y, lives):
        self.position_x = position_x
        self.position_y = position_y
        self.lives = lives

    def hit(self):
        self.lives -= 1

    def is_destroyed(self):
        return self.lives <= 0


class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = self.load_bricks()

    def load_bricks(self):
        bricks = []
        with open('bricks.txt', 'r') as file:
            for line in file:
                position_x, position_y, lives = map(int, line.strip().split('|'))
                bricks.append(Brick(position_x, position_y, lives))
        return bricks

    def run(self):
        # Main game loop
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

            self.ball.update()

            screen.fill((0, 0, 0))  # Clear screen
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw(self, screen):
        # Draw paddle
        pygame.draw.rect(screen, (255, 255, 255), (self.paddle.get_position(), 550, 100, 10))
        # Draw ball
        pygame.draw.circle(screen, (255, 255, 255), (self.ball.position_x, self.ball.position_y), 10)
        # Draw bricks
        for brick in self.bricks:
            if not brick.is_destroyed():
                pygame.draw.rect(screen, (255, 0, 0), (brick.position_x, brick.position_y, 60, 20))