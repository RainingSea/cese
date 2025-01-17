import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.paddle = Paddle(self.width // 2, 20, 100, 20)
        self.ball = Ball(self.width // 2, self.height // 2, 10)
        self.bricks = self.create_bricks()
        self.lives = 3
        self.load_game_data()

    def create_bricks(self):
        bricks = []
        for i in range(5):
            for j in range(10):
                brick = Brick(j * 80 + 10, i * 30 + 10, 1)
                bricks.append(brick)
        return bricks

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game_data()
                pygame.quit()
                exit()

    def update(self):
        self.ball.move()
        # Additional game logic for ball collision with paddle and bricks would go here

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
        pygame.display.flip()

    def load_game_data(self):
        try:
            with open('game_data.txt', 'r') as file:
                lines = file.readlines()
                self.lives = int(lines[0].strip())
                # Load other game state data if necessary
        except FileNotFoundError:
            self.lives = 3  # Default lives if file not found

    def save_game_data(self):
        with open('game_data.txt', 'w') as file:
            file.write(f"{self.lives}\n")
            # Save other game state data if necessary