import pygame
import random

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.is_paused = False
        self.high_score_manager = HighScoreManager('high_scores.txt')
        self.high_scores = self.high_score_manager.read_high_scores()

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause()
                    if event.key == pygame.K_r:
                        self.resume()

            if not self.is_paused:
                self.snake.move()
                if self.check_collision():
                    self.update_score()
                    self.food.reposition(self.snake.body)

            screen.fill((0, 0, 0))
            self.draw_elements(screen)
            pygame.display.flip()
            clock.tick(10)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def check_collision(self):
        return self.snake.body[0] == self.food.position

    def update_score(self):
        self.score += 1
        if self.score > max(self.high_scores, default=0):
            self.high_score_manager.write_high_score(self.score)

    def generate_food(self):
        pass  # Not needed as it's handled in Food class

    def draw_elements(self, screen):
        for segment in self.snake.body:
            pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], 10, 10))
        pygame.draw.rect(screen, (255, 0, 0), (self.food.position[0], self.food.position[1], 10, 10))
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'RIGHT'

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'RIGHT':
            head_x += 10
        elif self.direction == 'LEFT':
            head_x -= 10
        elif self.direction == 'UP':
            head_y -= 10
        elif self.direction == 'DOWN':
            head_y += 10
        self.body.insert(0, (head_x, head_y))
        self.body.pop()

    def grow(self):
        pass  # Not implemented for simplicity

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self):
        self.position = (random.randint(0, 59) * 10, random.randint(0, 39) * 10)

    def reposition(self, snake_body):
        while True:
            new_position = (random.randint(0, 59) * 10, random.randint(0, 39) * 10)
            if new_position not in snake_body:
                self.position = new_position
                break

class HighScoreManager:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_high_scores(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def write_high_score(self, score: int):
        with open(self.file_path, 'a') as file:
            file.write(f"{score}\n")