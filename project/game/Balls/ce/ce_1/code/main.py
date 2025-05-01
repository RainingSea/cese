import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
ENEMY_SIZE = 20
ENEMY_COUNT = 5

class PlayerBall:
    def __init__(self):
        self.size = PLAYER_SIZE
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def move(self, direction):
        x, y = self.position
        if direction == 'UP' and y - self.size > 0:
            self.position = (x, y - 5)
        elif direction == 'DOWN' and y + self.size < SCREEN_HEIGHT:
            self.position = (x, y + 5)
        elif direction == 'LEFT' and x - self.size > 0:
            self.position = (x - 5, y)
        elif direction == 'RIGHT' and x + self.size < SCREEN_WIDTH:
            self.position = (x + 5, y)

    def grow(self):
        self.size += 5

class EnemyBall:
    def __init__(self):
        self.size = ENEMY_SIZE
        self.position = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def move(self):
        # Simple movement logic for enemy balls
        self.position = (self.position[0] + random.choice([-1, 1]), self.position[1] + random.choice([-1, 1]))
        # Keep enemy balls within screen bounds
        self.position = (max(0, min(SCREEN_WIDTH, self.position[0])), max(0, min(SCREEN_HEIGHT, self.position[1])))

class Game:
    def __init__(self):
        self.player_ball = PlayerBall()
        self.enemy_balls = [EnemyBall() for _ in range(ENEMY_COUNT)]
        self.score = 0
        self.running = True

    def start(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ball Game")
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.update()
            self.check_collisions()
            self.render()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player_ball.move('UP')
                elif event.key == pygame.K_DOWN:
                    self.player_ball.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.player_ball.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.player_ball.move('RIGHT')

        for enemy in self.enemy_balls:
            enemy.move()

    def check_collisions(self):
        player_rect = pygame.Rect(self.player_ball.position[0], self.player_ball.position[1], self.player_ball.size, self.player_ball.size)
        for enemy in self.enemy_balls:
            enemy_rect = pygame.Rect(enemy.position[0], enemy.position[1], enemy.size, enemy.size)
            if player_rect.colliderect(enemy_rect):
                self.player_ball.grow()
                self.score += 1
                self.enemy_balls.remove(enemy)
                self.enemy_balls.append(EnemyBall())  # Respawn enemy ball

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, (0, 255, 0), self.player_ball.position, self.player_ball.size)
        for enemy in self.enemy_balls:
            pygame.draw.circle(self.screen, (255, 0, 0), enemy.position, enemy.size)
        pygame.display.flip()

    def end_game(self):
        pygame.quit()

class Main:
    @staticmethod
    def main():
        game = Game()
        game.start()
        game.end_game()

if __name__ == "__main__":
    Main.main()