import pygame
import random
from obstacle import Obstacle

class Game:
    def __init__(self):
        self.speed = 0
        self.distance = 0
        self.lane = 1
        self.obstacles = []
        self.load_game()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            self.update()
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def update(self):
        self.distance += self.speed / 60  # Update distance based on speed
        for obstacle in self.obstacles:
            obstacle.move()
            if self.check_collision(obstacle):
                self.save_game()
                pygame.quit()

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Clear screen with white
        # Draw player car (placeholder)
        pygame.draw.rect(screen, (0, 0, 255), (self.lane * 100, 500, 50, 100))
        # Draw obstacles
        for obstacle in self.obstacles:
            color = (255, 0, 0) if obstacle.type else (0, 255, 0)  # Red for slowing down, green for game over
            pygame.draw.rect(screen, color, (obstacle.position, 400, 50, 50))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.lane > 0:
                    self.lane -= 1
                if event.key == pygame.K_RIGHT and self.lane < 2:
                    self.lane += 1

    def check_collision(self, obstacle: Obstacle) -> bool:
        # Simple collision detection
        if obstacle.position > 450 and obstacle.position < 550 and self.lane * 100 == 100:
            return True
        return False

    def save_game(self):
        with open('game_data.txt', 'w') as f:
            f.write(f'speed|{self.speed}\ndistance|{self.distance}\nlane|{self.lane}\n')

    def load_game(self):
        try:
            with open('game_data.txt', 'r') as f:
                for line in f:
                    key, value = line.strip().split('|')
                    if key == 'speed':
                        self.speed = int(value)
                    elif key == 'distance':
                        self.distance = float(value)
                    elif key == 'lane':
                        self.lane = int(value)
        except FileNotFoundError:
            self.speed = 0
            self.distance = 0
            self.lane = 1