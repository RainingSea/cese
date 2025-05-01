import pygame
import random
import os

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
SNAKE_SIZE = 10
FPS = 15

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = self.load_high_score()
        self.is_paused = False

    def load_high_score(self):
        if os.path.exists('highscore.txt'):
            with open('highscore.txt', 'r') as file:
                return int(file.read())
        return 0

    def run(self):
        while True:
            self.handle_events()
            if not self.is_paused:
                self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)
                elif event.key == pygame.K_p:
                    self.is_paused = not self.is_paused

    def update(self):
        self.snake.move()
        if self.check_collision():
            self.game_over()
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.spawn()
            self.score += 1

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        self.display_score()
        if self.is_paused:
            self.pause_menu()
        pygame.display.flip()
        self.clock.tick(FPS)

    def check_collision(self):
        head_x, head_y = self.snake.get_head_position()
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        if len(self.snake.body) != len(set(self.snake.body)):
            return True
        return False

    def pause_menu(self):
        font = pygame.font.SysFont('Arial', 30)
        pause_text = font.render('Paused', True, (255, 255, 255))
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open('highscore.txt', 'w') as file:
                file.write(str(self.high_score))
        font = pygame.font.SysFont('Arial', 30)
        game_over_text = font.render('Game Over! Score: ' + str(self.score), True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        self.__init__()

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (10, 0)

    def move(self):
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)

    def get_head_position(self):
        return self.body[0]

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], SNAKE_SIZE, SNAKE_SIZE))

if __name__ == '__main__':
    Game().run()