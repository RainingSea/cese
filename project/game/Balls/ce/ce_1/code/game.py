import pygame
import random

class PlayerBall:
    def __init__(self, size: float, position: tuple):
        self.size = size
        self.position = list(position)

    def grow(self, amount: float) -> None:
        self.size += amount

    def move(self, direction: tuple) -> None:
        self.position[0] += direction[0]
        self.position[1] += direction[1]

class EnemyBall:
    def __init__(self, size: float, position: tuple):
        self.size = size
        self.position = list(position)

class Game:
    def __init__(self):
        self.player_ball = PlayerBall(size=10.0, position=[400, 300])
        self.enemy_balls = [EnemyBall(size=random.uniform(5, 15), position=[random.randint(0, 800), random.randint(0, 600)]) for _ in range(5)]
        self.score = 0

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battle of Balls")
        clock = pygame.time.Clock()

        self.initialize()

        running = True
        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            self.check_collisions()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def initialize(self) -> None:
        # Load game data from file
        self.load_game_data()

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        direction = [0, 0]
        if keys[pygame.K_LEFT]:
            direction[0] = -5
        if keys[pygame.K_RIGHT]:
            direction[0] = 5
        if keys[pygame.K_UP]:
            direction[1] = -5
        if keys[pygame.K_DOWN]:
            direction[1] = 5
        self.player_ball.move(direction)

    def update(self) -> None:
        # Update game state if needed
        pass

    def draw(self, screen) -> None:
        screen.fill((255, 255, 255))  # Clear screen
        pygame.draw.circle(screen, (0, 255, 0), (int(self.player_ball.position[0]), int(self.player_ball.position[1])), int(self.player_ball.size))
        for enemy in self.enemy_balls:
            pygame.draw.circle(screen, (255, 0, 0), (int(enemy.position[0]), int(enemy.position[1])), int(enemy.size))

    def check_collisions(self) -> None:
        for enemy in self.enemy_balls:
            if (self.player_ball.position[0] - enemy.position[0]) ** 2 + (self.player_ball.position[1] - enemy.position[1]) ** 2 < (self.player_ball.size + enemy.size) ** 2:
                self.player_ball.grow(enemy.size)
                self.score += 1
                self.enemy_balls.remove(enemy)
                break

    def load_game_data(self) -> None:
        try:
            with open('game_data.txt', 'r') as file:
                data = file.readlines()
                # Load player score and size, enemy positions
                # Example: "score|size|enemy_positions"
                self.score = int(data[0].split('|')[0])
                self.player_ball.size = float(data[0].split('|')[1])
                enemy_positions = data[0].split('|')[2].strip().split(';')
                for pos in enemy_positions:
                    size, x, y = map(float, pos.split(','))
                    self.enemy_balls.append(EnemyBall(size=size, position=(x, y)))
        except FileNotFoundError:
            pass  # Handle file not found case