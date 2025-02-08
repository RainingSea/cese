import pygame
from snake import Snake
from food import Food
from score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 400, 400
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.is_paused = False
        self.food.generate_food(self.snake.body)

    def run(self):
        while True:
            self.handle_events()
            if not self.is_paused:
                self.update()
            self.draw()
            self.clock.tick(10)  # Frame rate

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.direction = (1, 0)
                elif event.key == pygame.K_p:
                    self.pause()

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.score.increase()
            self.food.generate_food(self.snake.body)
        if self.snake.check_collision(wall=True):
            self.end_game()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(segment[0] * 20, segment[1] * 20, 20, 20))
        food_x, food_y = self.food.position
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(food_x * 20, food_y * 20, 20, 20))
        score_text = pygame.font.SysFont('Arial', 25).render(f'Score: {self.score.get_score()}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def pause(self):
        self.is_paused = not self.is_paused

    def end_game(self):
        pygame.quit()
        exit()