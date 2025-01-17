import pygame
import random

class PlayerBall:
    def __init__(self, size: int, x: int, y: int):
        self.size = size
        self.x = x
        self.y = y

    def move(self, direction: str) -> None:
        if direction == 'UP':
            self.y -= 5
        elif direction == 'DOWN':
            self.y += 5
        elif direction == 'LEFT':
            self.x -= 5
        elif direction == 'RIGHT':
            self.x += 5

    def grow(self, amount: int) -> None:
        self.size += amount


class EnemyBall:
    def __init__(self, size: int, x: int, y: int):
        self.size = size
        self.x = x
        self.y = y

    def move(self) -> None:
        self.y += 2  # Move downwards


class Game:
    def __init__(self):
        self.player_ball = PlayerBall(size=30, x=400, y=300)
        self.enemy_balls = []
        self.score = 0

    def run(self) -> None:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battle of Balls")
        clock = pygame.time.Clock()

        running = True
        while running:
            self.handle_input()
            self.update()
            self.check_collisions()
            self.spawn_enemy()

            screen.fill((0, 0, 0))  # Clear screen
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_ball.move('UP')
        if keys[pygame.K_DOWN]:
            self.player_ball.move('DOWN')
        if keys[pygame.K_LEFT]:
            self.player_ball.move('LEFT')
        if keys[pygame.K_RIGHT]:
            self.player_ball.move('RIGHT')

    def update(self) -> None:
        for enemy in self.enemy_balls:
            enemy.move()

    def check_collisions(self) -> None:
        for enemy in self.enemy_balls:
            if (self.player_ball.x < enemy.x + enemy.size and
                self.player_ball.x + self.player_ball.size > enemy.x and
                self.player_ball.y < enemy.y + enemy.size and
                self.player_ball.y + self.player_ball.size > enemy.y):
                self.player_ball.grow(5)
                self.enemy_balls.remove(enemy)
                self.score += 1

    def spawn_enemy(self) -> None:
        if random.randint(1, 30) == 1:  # Spawn an enemy ball randomly
            size = random.randint(10, 20)
            x = random.randint(0, 780)
            y = 0  # Start from the top
            new_enemy = EnemyBall(size, x, y)
            self.enemy_balls.append(new_enemy)

    def save_game_data(self) -> None:
        with open('game_data.txt', 'w') as file:
            file.write(f'Score: {self.score}\n')

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (self.player_ball.x, self.player_ball.y), self.player_ball.size)
        for enemy in self.enemy_balls:
            pygame.draw.circle(screen, (0, 0, 255), (enemy.x, enemy.y), enemy.size)